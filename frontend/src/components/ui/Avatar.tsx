/**
 * Avatar Component
 */

import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { User } from 'lucide-react';

interface AvatarProps {
  src?: string;
  alt?: string;
  name?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

const sizes = {
  sm: 'w-8 h-8 text-xs',
  md: 'w-10 h-10 text-sm',
  lg: 'w-12 h-12 text-base',
  xl: 'w-16 h-16 text-lg',
};

function getInitials(name: string): string {
  const parts = name.trim().split(/\s+/);
  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
}

function getColorFromName(name: string): string {
  const colors = [
    'bg-primary-500',
    'bg-secondary-500',
    'bg-blue-500',
    'bg-green-500',
    'bg-purple-500',
    'bg-pink-500',
    'bg-orange-500',
    'bg-teal-500',
  ];
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
}

export function Avatar({ src, alt, name, size = 'md', className }: AvatarProps) {
  const baseStyles =
    'relative inline-flex items-center justify-center rounded-full overflow-hidden flex-shrink-0';

  if (src) {
    return (
      <div className={twMerge(clsx(baseStyles, sizes[size], className))}>
        <img
          src={src}
          alt={alt || name || 'Avatar'}
          className="w-full h-full object-cover"
          onError={(e) => {
            // Hide broken image and show fallback
            (e.target as HTMLImageElement).style.display = 'none';
          }}
        />
      </div>
    );
  }

  if (name) {
    const initials = getInitials(name);
    const bgColor = getColorFromName(name);

    return (
      <div
        className={twMerge(
          clsx(baseStyles, sizes[size], bgColor, 'text-white font-semibold', className)
        )}
        title={name}
      >
        {initials}
      </div>
    );
  }

  return (
    <div
      className={twMerge(
        clsx(
          baseStyles,
          sizes[size],
          'bg-slate-200 dark:bg-slate-700 text-slate-500 dark:text-slate-400',
          className
        )
      )}
    >
      <User className="w-1/2 h-1/2" />
    </div>
  );
}
