/**
 * DocuTask Agent Design System - Border & Radius Tokens
 */

export const borders = {
  radius: {
    none: '0px',
    xs: '2px',
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    '2xl': '24px',
    full: '9999px',
  },

  width: {
    none: '0px',
    thin: '1px',
    medium: '2px',
    thick: '4px',
  },

  // Glassmorphic border treatment
  glass: '1px solid rgba(255, 255, 255, 0.08)',
  glassSubtle: '1px solid rgba(255, 255, 255, 0.04)',
  glassActive: '1px solid rgba(0, 210, 255, 0.4)',
} as const;

export type BorderToken = typeof borders;
