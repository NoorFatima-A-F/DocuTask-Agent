/**
 * DocuTask Agent Design System - Typography Tokens
 */

export const typography = {
  fontFamily: {
    sans: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    mono: '"JetBrains Mono", "Fira Code", Menlo, Monaco, Consolas, monospace',
  },

  fontSize: {
    xs: '0.75rem',     // 12px
    sm: '0.875rem',    // 14px
    base: '1rem',      // 16px
    lg: '1.125rem',    // 18px
    xl: '1.25rem',     // 20px
    '2xl': '1.5rem',   // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem',  // 36px
  },

  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },

  lineHeight: {
    tight: 1.25,
    snug: 1.375,
    normal: 1.5,
    relaxed: 1.625,
  },

  letterSpacing: {
    tight: '-0.025em',
    normal: '0em',
    wide: '0.025em',
    wider: '0.05em',
    widest: '0.1em',
  },

  // Specialized Presets
  presets: {
    agentThought: {
      fontFamily: '"JetBrains Mono", monospace',
      fontSize: '0.8125rem', // 13px
      lineHeight: 1.6,
      letterSpacing: '0.01em',
    },
    metricTabular: {
      fontFamily: '"JetBrains Mono", monospace',
      fontVariantNumeric: 'tabular-nums',
      fontWeight: 600,
    },
    missionHeading: {
      fontSize: '1.25rem',
      fontWeight: 700,
      letterSpacing: '-0.02em',
    }
  }
} as const;

export type TypographyToken = typeof typography;
