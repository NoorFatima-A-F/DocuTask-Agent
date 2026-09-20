/**
 * DocuTask Agent Design System - Animation Tokens & Timing
 */

export const animations = {
  duration: {
    instant: '50ms',
    fast: '150ms',
    normal: '250ms',
    slow: '400ms',
    deliberate: '700ms',
    pulse: '2000ms',
  },

  easing: {
    default: 'cubic-bezier(0.4, 0, 0.2, 1)',
    in: 'cubic-bezier(0.4, 0, 1, 1)',
    out: 'cubic-bezier(0, 0, 0.2, 1)',
    inOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    spring: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
  },

  // Keyframe CSS classes or definitions
  keyframes: {
    neuralPulse: `
      @keyframes neuralPulse {
        0%, 100% { opacity: 1; transform: scale(1); filter: drop-shadow(0 0 4px rgba(0, 210, 255, 0.4)); }
        50% { opacity: 0.6; transform: scale(0.97); filter: drop-shadow(0 0 12px rgba(0, 210, 255, 0.8)); }
      }
    `,
    radarSweep: `
      @keyframes radarSweep {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
    `,
    shimmer: `
      @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
      }
    `,
  },
} as const;

export type AnimationToken = typeof animations;
