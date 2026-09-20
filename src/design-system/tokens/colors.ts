/**
 * DocuTask Agent Design System - Color Tokens
 * 
 * Theme: Enterprise AI Coworker
 * Characteristics: Trustworthy, Intelligent, Modern, Premium, Explainable, Autonomous
 */

export const colors = {
  // Brand & Intelligence Accents
  brand: {
    primary: '#0066FF',      // Intelligent Cobalt
    primaryHover: '#0052CC',
    primaryGlow: 'rgba(0, 102, 255, 0.35)',
    secondary: '#00D2FF',    // Neural Cyan
    secondaryGlow: 'rgba(0, 210, 255, 0.25)',
    tertiary: '#6366F1',     // Deep Violet (Reasoning)
    gradient: 'linear-gradient(135deg, #0066FF 0%, #00D2FF 100%)',
    gradientSubtle: 'linear-gradient(135deg, rgba(0, 102, 255, 0.15) 0%, rgba(0, 210, 255, 0.05) 100%)',
  },

  // Agent Cognitive & Operational States
  agent: {
    idle: '#64748B',         // Slate 500 (Standby / Inactive)
    thinking: '#00D2FF',     // Neural Cyan Pulse (Observing / Deliberating)
    executing: '#0066FF',    // Cobalt (Active Action / Execution)
    verifying: '#8B5CF6',    // Purple (Cryptographic / SLSA Verification)
    learning: '#EC4899',     // Rose / Magenta (Memory Consolidation)
    waiting: '#F59E0B',      // Amber (Human-in-the-Loop Checkpoint)
    completed: '#10B981',    // Emerald (Mission Success)
    failed: '#EF4444',       // Crimson (Execution Failure / Regressed)
    aborted: '#94A3B8',      // Muted Slate (User Terminated)
  },

  // Zero-Fabrication Explicit Sentinels
  sentinel: {
    unknown: '#64748B',
    notAvailable: '#94A3B8',
    notCollected: '#A855F7',
    notExecuted: '#6B7280',
    insufficientContext: '#F59E0B',
    insufficientEvidence: '#F97316',
    capabilityUnavailable: '#E11D48',
    datasetUnavailable: '#D97706',
    resourceUnavailable: '#DC2626',
    pendingDiscovery: '#38BDF8',
  },

  // Semantic Status Tiers
  status: {
    success: '#10B981',
    successBg: 'rgba(16, 185, 129, 0.12)',
    successBorder: 'rgba(16, 185, 129, 0.25)',
    warning: '#F59E0B',
    warningBg: 'rgba(245, 158, 11, 0.12)',
    warningBorder: 'rgba(245, 158, 11, 0.25)',
    error: '#EF4444',
    errorBg: 'rgba(239, 68, 68, 0.12)',
    errorBorder: 'rgba(239, 68, 68, 0.25)',
    info: '#0066FF',
    infoBg: 'rgba(0, 102, 255, 0.12)',
    infoBorder: 'rgba(0, 102, 255, 0.25)',
  },

  // Enterprise Dark & Light Neutral Surfaces
  neutral: {
    bgApp: '#0A0F1D',        // Deepest Void Blue (Application Background)
    bgSurface: '#0F172A',    // Elevated Slate Surface
    bgSurfaceHover: '#1E293B',
    bgCard: '#131D35',       // Primary Card Glassmorphism base
    bgCardSubtle: '#182442',
    bgOverlay: 'rgba(10, 15, 29, 0.85)',
    
    borderSubtle: '#1E293B',
    borderMuted: '#334155',
    borderActive: '#0066FF',
    borderGlow: 'rgba(0, 210, 255, 0.4)',

    textPrimary: '#F8FAFC',
    textSecondary: '#94A3B8',
    textMuted: '#64748B',
    textInverse: '#0A0F1D',
  },

  // Statistical Confidence Bands
  confidence: {
    veryHigh: '#10B981',    // >= 95%
    high: '#34D399',        // 85% - 94%
    medium: '#FBBF24',      // 70% - 84%
    low: '#FB923C',         // 50% - 69%
    veryLow: '#F87171',     // < 50%
  }
} as const;

export type ColorToken = typeof colors;
