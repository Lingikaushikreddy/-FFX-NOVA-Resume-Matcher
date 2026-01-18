#!/bin/bash

# 1. Update README
git add README.md
git commit -m "docs: Update README with comprehensive project documentation and Phase 3 status"

# 2. Backend Resume Routes
git add api/routes/resume.py
git commit -m "feat(backend): Enhance resume route logic with better error handling"

# 3. Embedding Service
git add embeddings/service.py
git commit -m "feat(ai): Optimize embedding service configuration for performant cold starts"

# 4. Frontend Entry Point
git add frontend/index.html
git commit -m "feat(frontend): Update main entry point with proper SEO tags"

# 5. Frontend App Logic
git add frontend/src/App.tsx
git commit -m "feat(frontend): Refactor App.tsx layout to support dashboard routing"

# 6. Global Styles
git add frontend/src/index.css frontend/src/App.css
git commit -m "style(frontend): Update global styles with Tailwind v4 directives and animations"

# 7. API Client
git add frontend/src/api/
git commit -m "feat(frontend): Implement robust API client layer with type-safe responses"

# 8. Assets
git add frontend/src/assets/
git commit -m "feat(frontend): Add project assets and static resources"

# 9. TypeScript Types
git add frontend/src/types/
git commit -m "feat(frontend): Define core TypeScript interfaces for Job, Resume, and Match entities"

# 10. Forms Components
git add frontend/src/components/forms/
git commit -m "feat(frontend): Add reusable form components for input handling"

# 11. Layout Components
git add frontend/src/components/layout/
git commit -m "feat(frontend): Add layout components for consistent page structure"

# 12. UI Foundation
git add frontend/src/components/ui/
git commit -m "feat(frontend): Add UI foundation components (buttons, cards, badges)"

# 13. File Upload
git add frontend/src/components/FileUploadZone.tsx
git commit -m "feat(frontend): Add interactive File Upload Zone with drag-and-drop support"

# 14. Hero Section
git add frontend/src/components/HeroSection.tsx
git commit -m "feat(frontend): Add cinematic Hero Section with 3D particle effects"

# 15. Job Results Page
git add frontend/src/components/JobResultsPage.tsx
git commit -m "feat(frontend): Add Job Results Page for displaying match candidates"

# 16. Job Detail Modal
git add frontend/src/components/JobDetailModal.tsx
git commit -m "feat(frontend): Add Job Detail Modal for in-depth view of role requirements"

# 17. Job Match Grid
git add frontend/src/components/JobMatchGrid.tsx
git commit -m "feat(frontend): Add Job Match Grid component for visualized candidate ranking"

# 18. Filter Component
git add frontend/src/components/FilterSidebar.tsx
git commit -m "feat(frontend): Add Filter Sidebar for refining job search results"

# 19. Upskilling Enigne
git add frontend/src/components/UpskillingRecommendations.tsx
git commit -m "feat(frontend): Add Upskilling Recommendations component for skill gap analysis"

# 20. Scripts and Misc
git add scripts/seed_jobs.py
git add .
git commit -m "chore: Add job seeding script and finalize project structure"

echo "All 20 commits executed successfully!"
