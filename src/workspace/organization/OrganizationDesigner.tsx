import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Network,
  RotateCw,
  Sparkles,
  Users,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { VirtualOrganization, VirtualDepartment } from '../../types/organizationPlatform';

export const OrganizationDesigner: React.FC = () => {
  const [org, setOrg] = useState<VirtualOrganization | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [restructuring, setRestructuring] = useState<boolean>(false);
  const [selectedDept, setSelectedDept] = useState<VirtualDepartment | null>(null);

  const loadStructure = async () => {
    try {
      setLoading(true);
      const data = await organizationPlatformApiClient.getStructure();
      setOrg(data);
      if (data.departments.length > 0 && !selectedDept) {
        setSelectedDept(data.departments[0] || null);
      }
    } catch (err) {
      console.error('Failed to load organization structure:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStructure();
  }, []);

  const handleRestructure = async () => {
    try {
      setRestructuring(true);
      const res = await fetch('/api/v1/organization/restructure?org_id=org_enterprise_root', {
        method: 'POST',
      });
      const data = await res.json();
      setOrg(data);
    } catch (err) {
      console.error('Error restructuring organization:', err);
    } finally {
      setRestructuring(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg text-primary">
            <Network className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">AI Organization Designer</h1>
            <p className="text-sm text-muted-foreground">
              Dynamic Department Structuring, Autonomous Team Formation & Span-of-Control Optimization
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadStructure} disabled={loading}>
            <span className="flex items-center gap-2">
              <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={handleRestructure} disabled={restructuring}>
            <span className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              {restructuring ? 'Optimizing...' : 'Re-Optimize Hierarchy'}
            </span>
          </Button>
        </div>
      </div>

      {/* Top Topology Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="border-border shadow-sm">
          <CardContent className="p-4">
            <div className="text-xs text-muted-foreground">Operational Efficiency</div>
            <div className="text-2xl font-bold text-emerald-500 mt-1">
              {org ? `${(org.operational_efficiency * 100).toFixed(1)}%` : '95.0%'}
            </div>
            <p className="text-xs text-muted-foreground mt-0.5">Redundancy eliminated</p>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardContent className="p-4">
            <div className="text-xs text-muted-foreground">Span of Control</div>
            <div className="text-2xl font-bold text-primary mt-1">{org ? org.span_of_control : 3.8}</div>
            <p className="text-xs text-muted-foreground mt-0.5">Average teams per head</p>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardContent className="p-4">
            <div className="text-xs text-muted-foreground">Departments Formed</div>
            <div className="text-2xl font-bold mt-1">{org?.departments.length ?? 3}</div>
            <p className="text-xs text-muted-foreground mt-0.5">Active specialized units</p>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardContent className="p-4">
            <div className="text-xs text-muted-foreground">Executive Board</div>
            <div className="text-2xl font-bold text-purple-500 mt-1">{org?.executive_board.length ?? 3}</div>
            <p className="text-xs text-muted-foreground mt-0.5">CEO, CTO & CFO agents</p>
          </CardContent>
        </Card>
      </div>

      {/* Departments & Team Tree View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Department Tree */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold">Active Departments</h2>
          <div className="space-y-3">
            {org?.departments.map((d) => (
              <Card
                key={d.department_id}
                onClick={() => setSelectedDept(d)}
                className={`border cursor-pointer transition-all ${
                  selectedDept?.department_id === d.department_id
                    ? 'border-primary bg-primary/5 shadow-sm'
                    : 'border-border hover:bg-muted/30'
                }`}
              >
                <CardContent className="p-4 space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="font-semibold text-sm">{d.name}</span>
                    <Badge variant="outline">{d.head_role}</Badge>
                  </div>
                  <div className="flex items-center justify-between text-xs text-muted-foreground pt-1">
                    <span>Teams: {d.teams.length}</span>
                    <span className="text-emerald-500 font-medium">Health: {(d.health_score * 100).toFixed(0)}%</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Department Deep Dive */}
        <div className="lg:col-span-2 space-y-6">
          {selectedDept ? (
            <Card className="border-border shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between pb-3">
                <div>
                  <CardTitle className="text-lg">{selectedDept.name}</CardTitle>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    Lead: <span className="font-mono text-primary">{selectedDept.head_role}</span>
                  </p>
                </div>
                <div className="text-right text-xs">
                  <div className="text-muted-foreground">Budget Allocated:</div>
                  <div className="font-semibold text-sm">${selectedDept.budget_allocated_usd.toLocaleString()}</div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Capabilities */}
                <div>
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                    Department Capabilities
                  </h3>
                  <div className="flex flex-wrap gap-1.5">
                    {selectedDept.capabilities.map((cap) => (
                      <Badge key={cap} variant="intelligence">
                        {cap}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Teams Tree */}
                <div>
                  <h3 className="text-sm font-semibold mb-2 flex items-center gap-2">
                    <Users className="w-4 h-4 text-primary" />
                    Autonomous Teams ({selectedDept.teams.length})
                  </h3>
                  <div className="space-y-3">
                    {selectedDept.teams.map((t) => (
                      <div key={t.team_id} className="p-3 bg-muted/30 border border-border rounded-lg space-y-2 text-xs">
                        <div className="flex justify-between items-center">
                          <span className="font-semibold text-sm text-foreground">{t.name}</span>
                          <span className="text-emerald-500 font-medium">
                            Productivity: {(t.productivity_score * 100).toFixed(0)}%
                          </span>
                        </div>
                        <p className="text-muted-foreground">{t.mission_scope}</p>
                        <div className="flex items-center gap-4 text-muted-foreground pt-1 border-t border-border/60">
                          <span>Team Lead: <strong className="text-foreground">{t.lead_role}</strong></span>
                          <span>Active Tasks: <strong className="text-foreground">{t.active_task_count}</strong></span>
                          <span>Workers: <strong className="text-foreground">{t.member_agent_ids.length}</strong></span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card className="border-border shadow-sm p-8 text-center text-muted-foreground">
              Select a department to view autonomous teams and capability assignments.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
