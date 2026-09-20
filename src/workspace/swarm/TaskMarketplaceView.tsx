import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import {
  Users,
  PlusCircle,
} from 'lucide-react';

interface AuctionItem {
  id: string;
  name: string;
  type: string;
  maxBudget: number;
  deadlineSec: number;
  status: 'OPEN' | 'AWARDED' | 'CANCELLED';
  bids: Array<{ bidder: string; cost: number; latencyMs: number; score: number; status: string }>;
}

export const TaskMarketplaceView: React.FC = () => {
  const [auctions] = useState<AuctionItem[]>([
    {
      id: 'auc-001',
      name: 'Batch Document OCR & Entity Extraction (50 Pages)',
      type: 'WEIGHTED_UTILITY',
      maxBudget: 100.0,
      deadlineSec: 10.0,
      status: 'AWARDED',
      bids: [
        { bidder: 'agent-spec-ocr', cost: 65.0, latencyMs: 140, score: 0.942, status: 'ACCEPTED' },
        { bidder: 'agent-res-opt', cost: 80.0, latencyMs: 220, score: 0.810, status: 'REJECTED' },
      ],
    },
    {
      id: 'auc-002',
      name: 'Cryptographic Merkle Tree Proof Generator',
      type: 'FIRST_PRICE_SEALED',
      maxBudget: 45.0,
      deadlineSec: 5.0,
      status: 'AWARDED',
      bids: [
        { bidder: 'agent-val-sec', cost: 30.0, latencyMs: 80, score: 0.985, status: 'ACCEPTED' },
      ],
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Task Auction Marketplace</h1>
            <Badge variant="success" size="sm">
              MARKET LIQUID
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Decentralized task auctions, competitive agent bidding, Pareto-optimal utility scoring, and contract settlement.
          </p>
        </div>
        <Button variant="primary" size="sm">
          <PlusCircle className="w-3.5 h-3.5 mr-1.5" />
          Publish Auction Task
        </Button>
      </div>

      {/* Auctions List */}
      <div className="space-y-4">
        {auctions.map(auc => (
          <Card key={auc.id} className="p-5 border-border/60 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3">
              <div className="flex items-center gap-2">
                <Badge variant="outline" size="sm" className="font-mono">{auc.id}</Badge>
                <h3 className="font-bold text-sm">{auc.name}</h3>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="intelligence" size="sm">{auc.type}</Badge>
                <Badge variant="success" size="sm">{auc.status}</Badge>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
              <div className="p-2.5 rounded bg-muted/20 border border-border/30">
                <span className="text-[10px] text-muted-foreground block">Max Budget Cap</span>
                <span className="font-bold text-emerald-400">${auc.maxBudget} USD</span>
              </div>
              <div className="p-2.5 rounded bg-muted/20 border border-border/30">
                <span className="text-[10px] text-muted-foreground block">SLA Deadline</span>
                <span className="font-bold text-blue-400">{auc.deadlineSec}s</span>
              </div>
              <div className="p-2.5 rounded bg-muted/20 border border-border/30">
                <span className="text-[10px] text-muted-foreground block">Total Bids</span>
                <span className="font-bold text-purple-400">{auc.bids.length} Submitted</span>
              </div>
              <div className="p-2.5 rounded bg-muted/20 border border-border/30">
                <span className="text-[10px] text-muted-foreground block">Award Status</span>
                <span className="font-bold text-emerald-400">Settled & Locked</span>
              </div>
            </div>

            {/* Bids Table */}
            <div>
              <span className="text-xs font-semibold text-muted-foreground block mb-2">Agent Bidding Log</span>
              <div className="space-y-2">
                {auc.bids.map(b => (
                  <div
                    key={b.bidder}
                    className={`flex items-center justify-between p-3 rounded-lg border text-xs font-mono ${
                      b.status === 'ACCEPTED'
                        ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-300'
                        : 'bg-muted/10 border-border/20 text-muted-foreground'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <Users className="w-3.5 h-3.5" />
                      <span className="font-bold">{b.bidder}</span>
                    </div>

                    <div className="flex items-center gap-4">
                      <span>Cost: ${b.cost}</span>
                      <span>Latency: {b.latencyMs}ms</span>
                      <span className="font-semibold">Utility: {(b.score * 100).toFixed(1)}%</span>
                      <Badge variant={b.status === 'ACCEPTED' ? 'success' : 'default'} size="sm">
                        {b.status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
