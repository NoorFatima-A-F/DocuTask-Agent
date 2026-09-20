import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Scale,
  ShieldCheck,
  CheckCircle2,
  RefreshCw,
} from 'lucide-react';

interface ReviewItem {
  id: string;
  topic: string;
  consensusType: string;
  votes: Record<string, string>;
  approvalPct: number;
  dissentNotes: string[];
  reviewedAt: string;
}

export const ConsensusReviewCenter: React.FC = () => {
  const [isArbitrating, setIsArbitrating] = useState(false);
  const [arbitrationNotice, setArbitrationNotice] = useState<string | null>(null);

  const reviews: ReviewItem[] = [
    {
      id: 'rev-cache-invariance-01',
      topic: 'Speculative Tensor Layout Invariance in Enterprise Accounting Streams',
      consensusType: 'UNANIMOUS',
      votes: {
        'agent-peer-oracle-alpha': 'APPROVE',
        'agent-peer-oracle-beta': 'APPROVE',
        'agent-peer-oracle-gamma': 'APPROVE',
        'agent-peer-oracle-delta': 'APPROVE',
      },
      approvalPct: 100.0,
      dissentNotes: [],
      reviewedAt: '2026-09-12T18:42:00Z',
    },
    {
      id: 'rev-triadic-swarm-02',
      topic: 'Triadic Swarm Specialization Protocol Scalability',
      consensusType: 'SUPERMAJORITY',
      votes: {
        'agent-peer-oracle-alpha': 'APPROVE',
        'agent-peer-oracle-beta': 'APPROVE',
        'agent-peer-oracle-gamma': 'APPROVE',
        'agent-peer-oracle-delta': 'REJECT',
      },
      approvalPct: 75.0,
      dissentNotes: [
        'agent-peer-oracle-delta: Expresses concern over edge cases with network packet loss > 5%. Recommended safety boundary.',
      ],
      reviewedAt: '2026-09-12T16:15:00Z',
    },
  ];

  const handleArbitrate = () => {
    setIsArbitrating(true);
    setTimeout(() => {
      setIsArbitrating(false);
      setArbitrationNotice('Multi-Agent Tribunal convened: 4 of 4 agents cast affirmative Bayesian votes. Consensus officially certified.');
      setTimeout(() => setArbitrationNotice(null), 4000);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Scale className="w-6 h-6 text-amber-500" />
            Multi-Agent Peer Review & Consensus Tribunal
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Conducts independent multi-agent peer review tribunals, aggregates Bayesian belief consensus, and records minority dissents.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm" onClick={handleArbitrate} disabled={isArbitrating}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isArbitrating ? 'animate-spin' : ''}`} />
            {isArbitrating ? 'Convening Tribunal...' : 'Convene Review Tribunal'}
          </Button>
        </div>
      </div>

      {arbitrationNotice && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{arbitrationNotice}</span>
        </div>
      )}

      {/* Reviews List */}
      <div className="space-y-4">
        {reviews.map(review => (
          <Card key={review.id} className="p-5 space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-gray-100 dark:border-gray-800 pb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-amber-500 font-semibold">{review.id}</span>
                  <Badge variant={review.consensusType === 'UNANIMOUS' ? 'success' : 'warning'} size="sm">
                    {review.consensusType}
                  </Badge>
                </div>
                <h3 className="text-base font-semibold text-gray-900 dark:text-white mt-1">{review.topic}</h3>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="outline" size="sm">
                  Approval: <strong className="text-emerald-600 ml-1">{review.approvalPct}%</strong>
                </Badge>
              </div>
            </div>

            <div>
              <span className="text-xs font-semibold text-gray-500 uppercase">Tribunal Agent Ballots</span>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-2">
                {Object.entries(review.votes).map(([agent, vote]) => (
                  <div key={agent} className="p-2.5 bg-gray-50 dark:bg-gray-800/40 rounded border border-gray-100 dark:border-gray-700 text-xs">
                    <div className="font-mono text-[10px] text-gray-400 truncate">{agent}</div>
                    <div className="mt-1 flex items-center justify-between">
                      <span className="font-semibold text-gray-800 dark:text-gray-200">{vote}</span>
                      {vote === 'APPROVE' ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                      ) : (
                        <ShieldCheck className="w-3.5 h-3.5 text-amber-500" />
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {review.dissentNotes.length > 0 && (
              <div className="p-3 bg-amber-50/50 dark:bg-amber-950/20 rounded border border-amber-200 dark:border-amber-800/40 text-xs">
                <span className="font-semibold text-amber-900 dark:text-amber-300">Minority Dissenting Opinions:</span>
                <ul className="mt-1 list-disc list-inside text-amber-800 dark:text-amber-400 space-y-0.5">
                  {review.dissentNotes.map((d, i) => (
                    <li key={i}>{d}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="flex items-center justify-between text-xs text-gray-400 pt-1 border-t border-gray-100 dark:border-gray-800">
              <span>Arbitration Algorithm: Bayesian Aggregation</span>
              <span>Conducted: {new Date(review.reviewedAt).toLocaleString()}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
