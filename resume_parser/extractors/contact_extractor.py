"""
Contact information extraction module.

This module extracts contact details from resume text including
email addresses, phone numbers, locations, and LinkedIn profiles.
"""

import re
from typing import Optional
import logging

from resume_parser.models.resume import ContactInfo

logger = logging.getLogger(__name__)


# Regex patterns for contact information
EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

PHONE_PATTERNS = [
    # US formats
    r"\+?1?\s*[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    # International format
    r"\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}",
    # Simple format
    r"\d{3}[-.\s]\d{3}[-.\s]\d{4}",
]

LINKEDIN_PATTERNS = [
    r"linkedin\.com/in/[\w\-]+",
    r"linkedin\.com/pub/[\w\-/]+",
    r"linkedin:\s*[\w\-]+",
]

# US state abbreviations and names for location detection
US_STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
}


class ContactExtractor:
    """
    Extract contact information from resume text.

    Identifies and extracts email addresses, phone numbers,
    physical locations, LinkedIn profiles, and candidate names.

    Example:
        extractor = ContactExtractor()
        contact = extractor.extract("John Doe\\njohn@email.com\\n(555) 123-4567")
    """

    def __init__(self) -> None:
        """Initialize the contact extractor with compiled patterns."""
        self._email_pattern = re.compile(EMAIL_PATTERN, re.IGNORECASE)
        self._phone_patterns = [re.compile(p) for p in PHONE_PATTERNS]
        self._linkedin_patterns = [
            re.compile(p, re.IGNORECASE) for p in LINKEDIN_PATTERNS
        ]

    def extract(self, text: str, contact_section: Optional[str] = None) -> ContactInfo:
        """
        Extract all contact information from text.

        Args:
            text: Full resume text or contact section text.
            contact_section: Optional specific contact section content.

        Returns:
            ContactInfo object with extracted details.
        """
        # Prefer contact section if available, but also search full text
        search_text = contact_section if contact_section else text

        contact = ContactInfo(
            email=self._extract_email(search_text) or self._extract_email(text),
            phone=self._extract_phone(search_text) or self._extract_phone(text),
            location=self._extract_location(search_text) or self._extract_location(text),
            linkedin=self._extract_linkedin(search_text) or self._extract_linkedin(text),
            name=self._extract_name(text),
        )

        return contact

    def _extract_email(self, text: str) -> Optional[str]:
        """
        Extract email address from text.

        Args:
            text: Text to search.

        Returns:
            First valid email found, or None.
        """
        if not text:
            return None

        match = self._email_pattern.search(text)
        if match:
            email = match.group()
            # Basic validation
            if self._is_valid_email(email):
                return email.lower()

        return None

    def _is_valid_email(self, email: str) -> bool:
        """
        Validate an email address.

        Args:
            email: Email string to validate.

        Returns:
            True if email appears valid.
        """
        if not email:
            return False

        # Check for common invalid patterns
        invalid_domains = ["example.com", "test.com", "placeholder"]
        for invalid in invalid_domains:
            if invalid in email.lower():
                return False

        # Must have @ and at least one dot after @
        if "@" not in email:
            return False

        parts = email.split("@")
        if len(parts) != 2:
            return False

        domain = parts[1]
        if "." not in domain:
            return False

        return True

    def _extract_phone(self, text: str) -> Optional[str]:
        """
        Extract phone number from text.

        Args:
            text: Text to search.

        Returns:
            First valid phone number found, or None.
        """
        if not text:
            return None

        for pattern in self._phone_patterns:
            match = pattern.search(text)
            if match:
                phone = match.group()
                # Clean up the phone number
                phone = self._normalize_phone(phone)
                if self._is_valid_phone(phone):
                    return phone

        return None

    def _normalize_phone(self, phone: str) -> str:
        """
        Normalize a phone number to a consistent format.

        Args:
            phone: Raw phone number string.

        Returns:
            Normalized phone number.
        """
        # Remove all non-digit characters except +
        cleaned = re.sub(r"[^\d+]", "", phone)

        # If it's a US number without country code, it should have 10 digits
        if len(cleaned) == 10:
            return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"

        # If it starts with 1 and has 11 digits, format as US
        if len(cleaned) == 11 and cleaned.startswith("1"):
            return f"+1 ({cleaned[1:4]}) {cleaned[4:7]}-{cleaned[7:]}"

        # Return as-is for international numbers
        return phone

    def _is_valid_phone(self, phone: str) -> bool:
        """
        Validate a phone number.

        Args:
            phone: Phone number to validate.

        Returns:
            True if phone appears valid.
        """
        if not phone:
            return False

        # Extract just digits
        digits = re.sub(r"\D", "", phone)

        # Should have at least 7 digits (local) and at most 15 (international)
        if len(digits) < 7 or len(digits) > 15:
            return False

        return True

    def _extract_linkedin(self, text: str) -> Optional[str]:
        """
        Extract LinkedIn profile URL from text.

        Args:
            text: Text to search.

        Returns:
            LinkedIn URL or username, or None.
        """
        if not text:
            return None

        for pattern in self._linkedin_patterns:
            match = pattern.search(text)
            if match:
                linkedin = match.group()
                # Normalize to full URL
                if not linkedin.startswith("http"):
                    if "linkedin.com" in linkedin.lower():
                        linkedin = "https://" + linkedin
                    else:
                        # Just username
                        linkedin = f"https://linkedin.com/in/{linkedin.split(':')[-1].strip()}"
                return linkedin

        return None

    def _extract_location(self, text: str) -> Optional[str]:
        """
        Extract location/address from text.

        Args:
            text: Text to search.

        Returns:
            Location string, or None.
        """
        if not text:
            return None

        # Look for city, state patterns
        # Pattern: City, ST or City, State
        state_abbrevs = "|".join(US_STATES.keys())
        state_names = "|".join(US_STATES.values())

        patterns = [
            # City, ST 12345
            rf"([A-Za-z\s]+),\s*({state_abbrevs})\s*\d{{5}}(?:-\d{{4}})?",
            # City, ST
            rf"([A-Za-z\s]+),\s*({state_abbrevs})\b",
            # City, State
            rf"([A-Za-z\s]+),\s*({state_names})\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group().strip()
                return location

        return None

    def _extract_name(self, text: str) -> Optional[str]:
        """
        Extract candidate name from text.

        The name is typically at the very beginning of a resume,
        often in a larger font (which we can't detect from text).

        Args:
            text: Full resume text.

        Returns:
            Candidate name, or None.
        """
        if not text:
            return None

        lines = text.strip().split("\n")

        # Look at first few non-empty lines
        for line in lines[:5]:
            line = line.strip()
            if not line:
                continue

            # Skip if it looks like contact info
            if self._email_pattern.search(line):
                continue
            if any(p.search(line) for p in self._phone_patterns):
                continue

            # Skip if it contains common non-name words
            skip_words = [
                "resume", "cv", "curriculum", "address", "phone",
                "email", "linkedin", "objective", "summary",
            ]
            if any(word in line.lower() for word in skip_words):
                continue

            # Name is likely 2-4 words, mostly letters
            words = line.split()
            if 1 <= len(words) <= 5:
                # Check if words look like names (start with capital, mostly letters)
                name_like = all(
                    word[0].isupper() and word.replace(".", "").replace("-", "").isalpha()
                    for word in words
                    if word
                )
                if name_like:
                    return line

        return None
