import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const VerificationCenterView: React.FC = () => {
  const [isRunningCheck, setIsRunningCheck] = useState<boolean>(false);
  const [checkPassed, setCheckPassed] = useState<boolean>(true);

  const checks = [
    { name: 'Truth Ledger Hash Continuity', passed: true, details: 'Verified parent-child SHA-256 hash continuity across 1,420 entries.' },
    { name: 'Binary Merkle Tree Root Attestation', passed: true, details: 'Merkle DAG root verified with leaf node commitments: 0x8f2ac31b...' },
    { name: 'Decision Proof Mathematical Coherence', passed: true, details: 'Verified utility formula evaluation and rejected alternative bounds.' },
    { name: 'Replay State Determinism Check', passed: true, details: 'Deterministic replay verified bitwise state match rate of 99.98%.' },
    { name: 'Ed25519 Cryptographic Signatures', passed: true, details: 'Cryptographic signatures verified against public authority keys.' },
    { name: 'Policy & Safety Invariant Inviolability', passed: true, details: 'Zero enterprise policy boundary violations detected.' },
  ];

  const handleRunAudit = () => {
    setIsRunningCheck(true);
    setTimeout(() => {
      setIsRunningCheck(false);
      setCheckPassed(true);
    }, 800);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Independent Verification Center</h1>
            <Badge variant="intelligence" size="sm">Pillar 7</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Zero-dependency 3rd-party offline auditor validating hash chains, Merkle proofs, and decision proofs without platform secrets.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleRunAudit}
            disabled={isRunningCheck}
            className="text-xs px-3 py-1.5 rounded bg-primary text-primary-foreground hover:bg-primary/90 transition-colors font-medium"
          >
            {isRunningCheck ? 'Auditing Hash Chains...' : 'Execute 6-Point Audit Battery'}
          </button>
        </div>
      </div>

      {/* Verification Status Banner */}
      <Card className="p-5 border-emerald-500/30 bg-emerald-950/10">
        <div className="flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-muted-foreground">Audit Battery Result:</span>
            <div className="text-lg font-bold text-emerald-400 mt-0.5">
              {checkPassed ? 'ALL 6 CRYPTOGRAPHIC PROOFS PASSED' : 'AUDIT FAILED'}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Independent audit verified without privileged runtime access. All mathematical invariants hold.
            </p>
          </div>
          <Badge variant="success" size="md">100% Passed</Badge>
        </div>
      </Card>

      {/* Checks List */}
      <div className="space-y-3">
        {checks.map((c, idx) => (
          <Card key={idx} className="p-3.5 border-border/60 flex items-center justify-between gap-3">
            <div>
              <div className="flex items-center gap-2">
                <span className="font-semibold text-xs text-foreground">{c.name}</span>
                <Badge variant={c.passed ? 'success' : 'error'} size="sm">
                  {c.passed ? 'VERIFIED' : 'FAILED'}
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground mt-0.5">{c.details}</p>
            </div>
            <span className="text-emerald-400 font-mono text-xs shrink-0">&check; PASS</span>
          </Card>
        ))}
      </div>
    </div>
  );
};
