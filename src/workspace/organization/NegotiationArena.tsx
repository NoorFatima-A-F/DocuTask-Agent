import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Scale,
  RotateCw,
  Sparkles,
  CheckCircle2,
  ArrowRight,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { AgentNegotiation, AgentRoleType } from '../../types/organizationPlatform';

export const NegotiationArena: React.FC = () => {
  const [negotiations, setNegotiations] = useState<AgentNegotiation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [negotiating, setNegotiating] = useState<boolean>(false);
  const [selectedNeg, setSelectedNeg] = useState<AgentNegotiation | null>(null);

  // Form State
  const [initiator, setInitiator] = useState<AgentRoleType>('RESEARCH_AGENT');
  const [respondent, setRespondent] = useState<AgentRoleType>('OPERATIONS_AGENT');
  const [topic] = useState<string>('GPU Compute Allocation: Distillation vs Ingestion');
  const [resource, setResource] = useState<string>('GPU_SLOTS');
  const [units, setUnits] = useState<number>(16.0);
  const [rationale, setRationale] = useState<string>(
    'Urgent 4-bit model distillation experiments require temporary dedicated cluster burst.'
  );

  const loadNegotiations = async () => {
    try {
      setLoading(true);
      const data = await organizationPlatformApiClient.getNegotiations();
      setNegotiations(data);
      if (data.length > 0 && !selectedNeg) {
        setSelectedNeg(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load negotiations:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadNegotiations();
  }, []);

  const handleStartNegotiation = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setNegotiating(true);
      const res = await organizationPlatformApiClient.initiateNegotiation(
        initiator,
        respondent,
        topic,
        resource,
        units,
        rationale
      );
      await loadNegotiations();
      setSelectedNeg(res.negotiation);
    } catch (err) {
      console.error('Error in agent negotiation:', err);
    } finally {
      setNegotiating(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg text-primary">
            <Scale className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Multi-Agent Negotiation Arena</h1>
            <p className="text-sm text-muted-foreground">
              Game-Theoretic Dispute Resolution, Concession Bargaining & Automated Nash Equilibrium Settlements
            </p>
          </div>
        </div>
        <Button variant="outline" onClick={loadNegotiations} disabled={loading}>
          <span className="flex items-center gap-2">
            <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* Start Negotiation Form */}
      <Card className="border-border shadow-sm">
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Scale className="w-4 h-4 text-primary" />
            Initiate Inter-Agent Resource Dispute & Bargaining
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleStartNegotiation} className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              <div>
                <label className="text-xs text-muted-foreground">Initiating Agent</label>
                <select
                  value={initiator}
                  onChange={(e) => setInitiator(e.target.value as AgentRoleType)}
                  className="w-full mt-1 px-3 py-1.5 text-xs rounded border border-input bg-background"
                >
                  <option value="RESEARCH_AGENT">RESEARCH_AGENT</option>
                  <option value="ENGINEERING_AGENT">ENGINEERING_AGENT</option>
                  <option value="ANALYST_AGENT">ANALYST_AGENT</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-muted-foreground">Responding Agent</label>
                <select
                  value={respondent}
                  onChange={(e) => setRespondent(e.target.value as AgentRoleType)}
                  className="w-full mt-1 px-3 py-1.5 text-xs rounded border border-input bg-background"
                >
                  <option value="OPERATIONS_AGENT">OPERATIONS_AGENT</option>
                  <option value="FINANCE_AGENT">FINANCE_AGENT</option>
                  <option value="CTO_AGENT">CTO_AGENT</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-muted-foreground">Resource Type</label>
                <input
                  type="text"
                  value={resource}
                  onChange={(e) => setResource(e.target.value)}
                  className="w-full mt-1 px-3 py-1.5 text-xs rounded border border-input bg-background"
                />
              </div>
              <div>
                <label className="text-xs text-muted-foreground">Requested Units</label>
                <input
                  type="number"
                  value={units}
                  onChange={(e) => setUnits(Number(e.target.value))}
                  className="w-full mt-1 px-3 py-1.5 text-xs rounded border border-input bg-background"
                />
              </div>
            </div>
            <div>
              <label className="text-xs text-muted-foreground">Demand Rationale</label>
              <input
                type="text"
                value={rationale}
                onChange={(e) => setRationale(e.target.value)}
                className="w-full mt-1 px-3 py-1.5 text-xs rounded border border-input bg-background"
              />
            </div>
            <div className="flex justify-end pt-1">
              <Button type="submit" variant="intelligence" disabled={negotiating}>
                <span className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4" />
                  {negotiating ? 'Solving Nash Equilibrium...' : 'Simulate & Solve Bargaining Session'}
                </span>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Main Two-Column View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Negotiation History */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold">Negotiation Logs ({negotiations.length})</h2>
          <div className="space-y-3">
            {negotiations.map((n) => (
              <Card
                key={n.negotiation_id}
                onClick={() => setSelectedNeg(n)}
                className={`border cursor-pointer transition-all ${
                  selectedNeg?.negotiation_id === n.negotiation_id
                    ? 'border-primary bg-primary/5 shadow-sm'
                    : 'border-border hover:bg-muted/30'
                }`}
              >
                <CardContent className="p-4 space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="font-semibold text-sm line-clamp-1">{n.topic}</span>
                    <Badge variant={n.status === 'RESOLVED' ? 'success' : 'warning'}>{n.status}</Badge>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <Badge variant="outline">{n.initiating_role}</Badge>
                    <ArrowRight className="w-3 h-3" />
                    <Badge variant="outline">{n.responding_role}</Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Negotiation Transcript & Agreement */}
        <div className="lg:col-span-2 space-y-6">
          {selectedNeg ? (
            <Card className="border-border shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between pb-3">
                <div>
                  <CardTitle className="text-lg">{selectedNeg.topic}</CardTitle>
                  <p className="text-xs text-muted-foreground font-mono mt-0.5">{selectedNeg.negotiation_id}</p>
                </div>
                <Badge variant={selectedNeg.status === 'RESOLVED' ? 'success' : 'warning'}>
                  {selectedNeg.status}
                </Badge>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Proposals Stream */}
                <div className="space-y-3">
                  <div className="p-3 bg-primary/5 border border-primary/20 rounded-lg text-xs space-y-1">
                    <div className="flex justify-between font-semibold text-primary">
                      <span>Initial Proposal: {selectedNeg.initiating_role}</span>
                      <span>Demand: {selectedNeg.proposals[0]?.requested_units} units</span>
                    </div>
                    <p className="text-muted-foreground">{selectedNeg.proposals[0]?.rationale}</p>
                  </div>

                  {selectedNeg.counter_proposals.map((cp) => (
                    <div key={cp.counter_id} className="p-3 bg-muted/40 border border-border rounded-lg text-xs space-y-1">
                      <div className="flex justify-between font-semibold text-foreground">
                        <span>Counter Offer: {cp.responding_role}</span>
                        <span>Offered: {cp.offered_units} units</span>
                      </div>
                      <ul className="list-disc pl-4 text-muted-foreground space-y-0.5">
                        {cp.compromise_conditions.map((c, i) => (
                          <li key={i}>{c}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>

                {/* Nash Settlement Card */}
                {selectedNeg.agreement && (
                  <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-sm text-emerald-500 flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4" /> Nash Bargaining Equilibrium Settlement
                      </span>
                      <Badge variant="success">
                        Nash Score: {(selectedNeg.agreement.nash_product_score * 100).toFixed(0)}%
                      </Badge>
                    </div>
                    <p className="text-xs text-foreground font-medium">
                      {selectedNeg.agreement.compromise_summary}
                    </p>
                    <div className="text-xs text-muted-foreground pt-1 border-t border-emerald-500/20">
                      Settled Allocation: <strong className="text-foreground">{selectedNeg.agreement.settled_units} units</strong> (Pareto Optimal)
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card className="border-border shadow-sm p-8 text-center text-muted-foreground">
              Select a negotiation log to inspect proposal rounds and Nash agreements.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
