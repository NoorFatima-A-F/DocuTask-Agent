import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Target,
  Plus,
  CheckCircle2,
  RotateCw,
  Sparkles,
  Calendar,
  Layers,
  ShieldAlert,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { Mission } from '../../types/organizationPlatform';

export const MissionControlCenter: React.FC = () => {
  const [missions, setMissions] = useState<Mission[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedMission, setSelectedMission] = useState<Mission | null>(null);
  const [newGoal, setNewGoal] = useState<string>('');
  const [timelineDays, setTimelineDays] = useState<number>(90);
  const [creating, setCreating] = useState<boolean>(false);
  const [validating, setValidating] = useState<boolean>(false);
  const [validationResult, setValidationResult] = useState<Record<string, any> | null>(null);

  const loadMissions = async () => {
    try {
      setLoading(true);
      const data = await organizationPlatformApiClient.getMissions();
      setMissions(data);
      if (data.length > 0 && !selectedMission) {
        setSelectedMission(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load missions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMissions();
  }, []);

  const handleCreateMission = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newGoal.trim()) return;
    try {
      setCreating(true);
      const created = await organizationPlatformApiClient.createMission(newGoal, 'HIGH', timelineDays);
      setNewGoal('');
      await loadMissions();
      setSelectedMission(created);
    } catch (err) {
      console.error('Failed to create mission:', err);
    } finally {
      setCreating(false);
    }
  };

  const handleValidate = async (missionId: string) => {
    try {
      setValidating(true);
      const res = await organizationPlatformApiClient.validateMission(missionId);
      setValidationResult(res);
      await loadMissions();
    } catch (err) {
      console.error('Failed to validate mission:', err);
    } finally {
      setValidating(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg text-primary">
            <Target className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Mission Understanding & Control</h1>
            <p className="text-sm text-muted-foreground">
              Autonomous Goal Decomposition, Mathematical Constraint Bounds & Strategic KPI Derivation
            </p>
          </div>
        </div>
        <Button variant="outline" onClick={loadMissions} disabled={loading}>
          <span className="flex items-center gap-2">
            <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* Goal Decomposition Form */}
      <Card className="border-border shadow-sm">
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-primary" />
            Decompose Natural Language Enterprise Goal
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleCreateMission} className="space-y-4">
            <div className="flex flex-col md:flex-row gap-4">
              <input
                type="text"
                value={newGoal}
                onChange={(e) => setNewGoal(e.target.value)}
                placeholder="e.g. Reduce document processing cost by 40% while maintaining >=98% accuracy"
                className="flex-1 px-3.5 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-1 focus:ring-primary"
              />
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground whitespace-nowrap">Timeline (Days):</span>
                <input
                  type="number"
                  value={timelineDays}
                  onChange={(e) => setTimelineDays(Number(e.target.value))}
                  min={7}
                  max={365}
                  className="w-20 px-2.5 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
              <Button type="submit" variant="primary" disabled={creating || !newGoal.trim()}>
                <span className="flex items-center gap-2">
                  <Plus className="w-4 h-4" />
                  {creating ? 'Decomposing...' : 'Decompose Goal'}
                </span>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Main Two-Column View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Mission List */}
        <Card className="border-border shadow-sm">
          <CardHeader>
            <CardTitle className="text-base flex items-center justify-between">
              <span>Active Missions ({missions.length})</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {missions.map((m) => (
              <div
                key={m.mission_id}
                onClick={() => {
                  setSelectedMission(m);
                  setValidationResult(null);
                }}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  selectedMission?.mission_id === m.mission_id
                    ? 'border-primary bg-primary/5 shadow-sm'
                    : 'border-border hover:bg-muted/40'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <span className="font-semibold text-sm line-clamp-1">{m.title}</span>
                  <Badge variant={m.priority === 'CRITICAL' ? 'error' : 'intelligence'}>{m.priority}</Badge>
                </div>
                <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{m.raw_goal}</p>
                <div className="flex items-center gap-3 mt-2 text-xs text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3.5 h-3.5" /> {m.timeline_days}d
                  </span>
                  <span className="flex items-center gap-1">
                    <Layers className="w-3.5 h-3.5" /> {m.objectives.length} Objectives
                  </span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Mission Detail View */}
        <div className="lg:col-span-2 space-y-6">
          {selectedMission ? (
            <>
              <Card className="border-border shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between pb-3">
                  <div>
                    <CardTitle className="text-lg">{selectedMission.title}</CardTitle>
                    <p className="text-xs text-muted-foreground font-mono mt-0.5">{selectedMission.mission_id}</p>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => handleValidate(selectedMission.mission_id)}
                    disabled={validating}
                  >
                    <span className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                      {validating ? 'Validating...' : 'Validate Feasibility'}
                    </span>
                  </Button>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Validation Feedback */}
                  {validationResult && (
                    <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-xs space-y-1">
                      <div className="font-semibold text-emerald-500 flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4" /> Mission Strategically Validated & Approved
                      </div>
                      <div className="text-muted-foreground">
                        Confidence: {(validationResult.confidence_score * 100).toFixed(1)}% | Alignment:{' '}
                        {(validationResult.alignment_score * 100).toFixed(1)}%
                      </div>
                    </div>
                  )}

                  {/* Objectives */}
                  <div>
                    <h3 className="text-sm font-semibold mb-2 flex items-center gap-2">
                      <Target className="w-4 h-4 text-primary" />
                      Decomposed Objectives ({selectedMission.objectives.length})
                    </h3>
                    <div className="space-y-2">
                      {selectedMission.objectives.map((obj) => (
                        <div key={obj.objective_id} className="p-3 bg-muted/30 border border-border rounded-lg text-sm">
                          <div className="flex justify-between items-start">
                            <span className="font-medium">{obj.title}</span>
                            <Badge variant="outline">{obj.status}</Badge>
                          </div>
                          <p className="text-xs text-muted-foreground mt-1">{obj.description}</p>
                          <div className="mt-2 flex items-center gap-4 text-xs text-muted-foreground">
                            <span>Target: {obj.target_value} ({obj.target_metric})</span>
                            <span>Progress: {obj.progress_percent}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Constraints */}
                  <div>
                    <h3 className="text-sm font-semibold mb-2 flex items-center gap-2">
                      <ShieldAlert className="w-4 h-4 text-amber-500" />
                      Hard & Soft Constraints ({selectedMission.constraints.length})
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {selectedMission.constraints.map((c) => (
                        <div key={c.constraint_id} className="p-2.5 bg-card border border-border rounded-lg text-xs">
                          <div className="flex justify-between items-center">
                            <Badge variant={c.is_strict ? 'error' : 'warning'}>
                              {c.is_strict ? 'STRICT' : 'FLEXIBLE'}
                            </Badge>
                            <span className="font-mono text-muted-foreground">
                              {c.threshold_value} {c.unit}
                            </span>
                          </div>
                          <p className="mt-1 font-medium">{c.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card className="border-border shadow-sm p-8 text-center text-muted-foreground">
              Select a mission to inspect objectives and constraints.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
