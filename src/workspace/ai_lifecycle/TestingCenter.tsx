import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import type { AgentTestResult } from '../../types/aiLifecycle';
import { TestTube2, CheckCircle2, ShieldCheck, Zap, RefreshCw } from 'lucide-react';

export const TestingCenter: React.FC = () => {
  const [testResult, setTestResult] = useState<AgentTestResult | null>(null);
  const [running, setRunning] = useState(false);

  const executeTest = async () => {
    setRunning(true);
    const res = await AILifecycleApiClient.runTests('agt_acme_invoice_reconciler', '1.2.0');
    setTestResult(res);
    setRunning(false);
  };

  useEffect(() => {
    executeTest();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <TestTube2 className="w-7 h-7 text-indigo-400" />
            AI Quality, Grounding & Performance Testing Harness
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Automated LLM Judge evaluation for factual grounding, hallucination scoring, and latency assertions.
          </p>
        </div>
        <Button variant="intelligence" onClick={executeTest} disabled={running}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${running ? 'animate-spin' : ''}`} /> Run Test Suite
          </span>
        </Button>
      </div>

      {testResult && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="bg-slate-900/80 border-slate-800">
            <CardContent className="p-4 flex items-center gap-3">
              <CheckCircle2 className="w-6 h-6 text-emerald-400" />
              <div>
                <span className="text-xs text-slate-400 block">Grounding Score</span>
                <span className="text-xl font-bold text-white">{(testResult.grounding_score * 100).toFixed(1)}%</span>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/80 border-slate-800">
            <CardContent className="p-4 flex items-center gap-3">
              <ShieldCheck className="w-6 h-6 text-indigo-400" />
              <div>
                <span className="text-xs text-slate-400 block">Hallucination Rate</span>
                <span className="text-xl font-bold text-emerald-400">{testResult.hallucination_rate_pct}%</span>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/80 border-slate-800">
            <CardContent className="p-4 flex items-center gap-3">
              <Zap className="w-6 h-6 text-amber-400" />
              <div>
                <span className="text-xs text-slate-400 block">P95 Latency</span>
                <span className="text-xl font-bold text-white">{testResult.latency_p95_ms} ms</span>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/80 border-slate-800">
            <CardContent className="p-4 flex items-center gap-3">
              <CheckCircle2 className="w-6 h-6 text-cyan-400" />
              <div>
                <span className="text-xs text-slate-400 block">Overall Status</span>
                <Badge variant="success" className="mt-1">{testResult.status}</Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
