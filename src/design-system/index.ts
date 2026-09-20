/**
 * DocuTask Agent Design System - Barrel Export
 */

export * from './tokens/colors';
export * from './tokens/typography';
export * from './tokens/spacing';
export * from './tokens/shadows';
export * from './tokens/borders';
export * from './tokens/animations';
export * from './tokens/polish';

import { colors } from './tokens/colors';
import { typography } from './tokens/typography';
import { spacing, layout } from './tokens/spacing';
import { shadows } from './tokens/shadows';
import { borders } from './tokens/borders';
import { animations } from './tokens/animations';
import { polishTokens } from './tokens/polish';

export const designTokens = {
  colors,
  typography,
  spacing,
  layout,
  shadows,
  borders,
  animations,
  polish: polishTokens,
} as const;

export type DesignTokens = typeof designTokens;
export default designTokens;
