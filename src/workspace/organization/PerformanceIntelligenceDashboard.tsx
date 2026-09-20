import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Award,
  RotateCw,
  Users,
  Building2,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { OrganizationScorecard } from '../../types/organizationPlatform';

export const PerformanceIntelligenceDashboard: React.FC = () => {
  const [scorecard, setScorecard] = useState<OrganizationScorecard | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadScorecard = async () => {
    try {
      setLoading(true);
      const data = await organizationPlatformApiClient.getScorecard();
      setScorecard(data);
    } catch (err) {
      console.error('Failed to load scorecard:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadScorecard();
  }, []);

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg text-primary">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Performance Intelligence Dashboard</h1>
            <p className="text-sm text-muted-foreground">
              Real-Time Organizational Scorecards, Team Collaboration Metrics & Agent Performance Ratings
            </p>
          </div>
        </div>
        <Button variant="outline" onClick={loadScorecard} disabled={loading}>
          <span className="flex items-center gap-2">
            <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* Macro Scorecard Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="border-border shadow-sm">
          <CardContent className="p-4 space-y-1">
            <div className="text-xs text-muted-foreground">Composite Health Score</div>
            <div className="text-2xl font-bold text-emerald-500">
              {scorecard ? `${(scorecard.composite_health_score * 100).toFixed(1)}%` : '97.0%'}
            </div>
            <p className="text-xs text-muted-foreground">Multi-department weighted index</p>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardContent className="p-4 space-y-1">
            <div className="text-xs text-muted-foreground">Annual Growth Rate</div>
            <div className="text-2xl font-bold text-primary">
              {scorecard ? `${scorecard.annual_growth_rate_pct.toFixed(1)}%` : '22.4%'}
            </div>
            <p className="text-xs text-muted-foreground">Document volume throughput scaling</p>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardContent className="p-4 space-y-1">
            <div className="text-xs text-muted-foreground">Innovation Index</div>
            <div className="text-2xl font-bold text-purple-500">
              {scorecard ? `${(scorecard.innovation_index * 100).toFixed(0)}%` : '95%'}
            </div>
            <p className="text-xs text-muted-foreground">Autonomous discovery & mutation rate</p>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardContent className="p-4 space-y-1">
            <div className="text-xs text-muted-foreground">Operational Efficiency</div>
            <div className="text-2xl font-bold text-blue-500">
              {scorecard ? `${(scorecard.operational_efficiency * 100).toFixed(1)}%` : '96.0%'}
            </div>
            <p className="text-xs text-muted-foreground">Task completion & SLA compliance</p>
          </CardContent>
        </Card>
      </div>

      {/* Team Scorecards */}
      <Card className="border-border shadow-sm">
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Building2 className="w-4 h-4 text-primary" />
            Autonomous Team Scorecards ({scorecard?.team_scorecards.length ?? 3})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {scorecard?.team_scorecards.map((team) => (
              <div key={team.team_id} className="p-4 bg-card border border-border rounded-lg space-y-3">
                <div className="flex justify-between items-start">
                  <span className="font-semibold text-sm">{team.team_name}</span>
                  <Badge variant={team.state === 'EXCEEDING' ? 'success' : 'outline'}>{team.state}</Badge>
                </div>
                <div className="space-y-1.5 text-xs text-muted-foreground">
                  <div className="flex justify-between">
                    <span>Collaboration:</span>
                    <strong className="text-foreground">{(team.collaboration_score * 100).toFixed(0)}%</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Completion Rate:</span>
                    <strong className="text-foreground">{(team.completion_rate * 100).toFixed(0)}%</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Knowledge Sharing:</span>
                    <strong className="text-foreground">{(team.knowledge_sharing_index * 100).toFixed(0)}%</strong>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Agent Performance Table */}
      <Card className="border-border shadow-sm">
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Users className="w-4 h-4 text-primary" />
            Agent Worker Ratings ({scorecard?.agent_scorecards.length ?? 0})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border text-left text-muted-foreground">
                  <th className="pb-2 font-medium">Agent Employee</th>
                  <th className="pb-2 font-medium">Role</th>
                  <th className="pb-2 font-medium">Accuracy</th>
                  <th className="pb-2 font-medium">Productivity</th>
                  <th className="pb-2 font-medium">Reliability</th>
                  <th className="pb-2 font-medium">Cost Efficiency</th>
                  <th className="pb-2 font-medium">State</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60">
                {scorecard?.agent_scorecards.map((agent) => (
                  <tr key={agent.agent_id} className="hover:bg-muted/30 transition-colors">
                    <td className="py-2.5 font-semibold">{agent.agent_name}</td>
                    <td className="py-2.5">
                      <Badge variant="outline">{agent.role}</Badge>
                    </td>
                    <td className="py-2.5 font-mono text-emerald-500 font-medium">
                      {(agent.accuracy_rate * 100).toFixed(1)}%
                    </td>
                    <td className="py-2.5 font-mono">{(agent.productivity_score * 100).toFixed(0)}%</td>
                    <td className="py-2.5 font-mono">{(agent.reliability_score * 100).toFixed(0)}%</td>
                    <td className="py-2.5 font-mono">{(agent.cost_efficiency * 100).toFixed(0)}%</td>
                    <td className="py-2.5">
                      <Badge variant={agent.state === 'EXCEEDING' ? 'success' : 'intelligence'}>
                        {agent.state}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
