import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Undo2,
  RotateCw,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { RollbackSession } from '../../types/executionPlatform';

export const RollbackRecoveryCenter: React.FC = () => {
  const [rollbacks, setRollbacks] = useState<RollbackSession[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadRollbacks = async () => {
    try {
      setLoading(true);
      const res = await executionPlatformApiClient.listRollbacks();
      setRollbacks(res.rollbacks || []);
    } catch (err) {
      console.error('Failed to load rollbacks:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRollbacks();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Undo2 className="w-5 h-5 text-rose-400" />
            Saga Rollback & Checkpoint Recovery Center
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated compensating transaction dispatcher, LIFO inverse execution & zero-residue cleanup
          </p>
        </div>
        <Button variant="outline" onClick={loadRollbacks}>
          <span className="flex items-center gap-2">
            <RotateCw className="w-4 h-4" />
            Refresh
          </span>
        </Button>
      </div>

      {/* Rollback Sessions List */}
      <Card className="bg-slate-900/60 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white">
            Compensating Rollback Sessions ({rollbacks.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading && rollbacks.length === 0 ? (
            <div className="py-8 text-center text-xs text-slate-500">Loading rollbacks...</div>
          ) : rollbacks.length === 0 ? (
            <div className="py-12 text-center text-sm text-slate-500">
              No rollback events recorded. All production execution pipelines have completed with clean invariants.
            </div>
          ) : (
            <div className="space-y-4">
              {rollbacks.map((rb) => (
                <div
                  key={rb.rollback_id}
                  className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3"
                >
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold text-white">{rb.trigger_reason}</span>
                        <Badge variant={rb.status === 'completed' ? 'success' : 'error'}>
                          {rb.status.toUpperCase()}
                        </Badge>
                      </div>
                      <p className="text-xs text-slate-400 font-mono mt-1">
                        Rollback ID: {rb.rollback_id} • Mission: {rb.mission_id}
                      </p>
                    </div>
                    <span className="text-xs text-slate-400">
                      {rb.completed_compensations} / {rb.steps_to_compensate.length} Inverses Executed
                    </span>
                  </div>

                  {/* Compensated Steps Sub-list */}
                  <div className="pl-4 border-l-2 border-rose-800/60 space-y-2">
                    {rb.steps_to_compensate.map((step) => (
                      <div
                        key={step.compensation_id}
                        className="p-2.5 bg-slate-900/80 rounded-lg border border-slate-800 flex items-center justify-between text-xs"
                      >
                        <div className="flex items-center gap-2">
                          <Undo2 className="w-3.5 h-3.5 text-rose-400" />
                          <span className="text-slate-200">
                            Undoing: <span className="font-mono text-purple-300">{step.original_step_id}</span>
                          </span>
                          <span className="text-slate-500">via</span>
                          <span className="font-mono text-slate-400">{step.compensation_tool_id}</span>
                        </div>
                        <Badge variant="success">{step.status}</Badge>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
