/**
 * DocuTask Agent Design System - Polish & Micro-Interaction Tokens
 */
export const polishTokens = {
    // Trust State Styling
    trustStates: {
        VERIFIED: {
            color: '#10B981',
            bg: 'rgba(16, 185, 129, 0.12)',
            border: 'rgba(16, 185, 129, 0.3)',
            icon: '✓',
            label: 'Cryptographically Verified',
        },
        EMPIRICAL: {
            color: '#00D2FF',
            bg: 'rgba(0, 210, 255, 0.12)',
            border: 'rgba(0, 210, 255, 0.3)',
            icon: '📊',
            label: 'Empirical Observation',
        },
        OBSERVED: {
            color: '#38BDF8',
            bg: 'rgba(56, 189, 248, 0.12)',
            border: 'rgba(56, 189, 248, 0.3)',
            icon: '👁️',
            label: 'Observed Telemetry',
        },
        ESTIMATED: {
            color: '#F59E0B',
            bg: 'rgba(245, 158, 11, 0.12)',
            border: 'rgba(245, 158, 11, 0.3)',
            icon: '≈',
            label: 'Statistical Estimate',
        },
        UNKNOWN: {
            color: '#94A3B8',
            bg: 'rgba(148, 163, 184, 0.12)',
            border: 'rgba(148, 163, 184, 0.3)',
            icon: '?',
            label: 'Zero-Fabrication Unknown',
        },
        INSUFFICIENT_EVIDENCE: {
            color: '#F97316',
            bg: 'rgba(249, 115, 22, 0.12)',
            border: 'rgba(249, 115, 22, 0.3)',
            icon: '⚠',
            label: 'Insufficient Evidence',
        },
    },
    // Personality & Avatars
    agentAvatars: {
        PLANNER: {
            avatarBg: 'from-blue-600 to-indigo-600',
            tagline: 'Formulating adaptive graph topologies',
            icon: '📐',
        },
        EVIDENCE: {
            avatarBg: 'from-cyan-500 to-blue-600',
            tagline: 'Auditing empirical observation digests',
            icon: '🔬',
        },
        MEMORY: {
            avatarBg: 'from-purple-600 to-pink-600',
            tagline: 'Consolidating long-term retention decay',
            icon: '🧠',
        },
        EXTRACTION: {
            avatarBg: 'from-emerald-500 to-teal-600',
            tagline: 'Running closed-loop Bayesian tuning',
            icon: '⚡',
        },
        REFLECTION: {
            avatarBg: 'from-pink-500 to-rose-600',
            tagline: 'Cross-validating p-values & effect sizes',
            icon: '🪞',
        },
        STATISTICS: {
            avatarBg: 'from-amber-500 to-orange-600',
            tagline: 'Verifying sample power thresholds',
            icon: '📈',
        },
        GOVERNANCE: {
            avatarBg: 'from-violet-600 to-purple-800',
            tagline: 'Auditing SLSA L3+ digital signatures',
            icon: '🛡️',
        },
        COORDINATOR: {
            avatarBg: 'from-cyan-400 to-blue-700',
            tagline: 'Harmonizing multi-agent consensus',
            icon: '🌐',
        },
    },
    // Delight & Celebration Timings
    delight: {
        confettiDurationMs: 4000,
        toastDismissMs: 3500,
    },
};
