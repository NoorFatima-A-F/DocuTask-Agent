import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import type { AgentSecurityScan } from '../../types/aiLifecycle';
import { ShieldAlert, CheckCircle2, AlertTriangle, RefreshCw } from 'lucide-react';

export const SecurityReviewCenter: React.FC = () => {
  const [scan, setScan] = useState<AgentSecurityScan | null>(null);
  const [scanning, setScanning] = useState(false);

  const runScan = async () => {
    setScanning(true);
    const res = await AILifecycleApiClient.scanSecurity('agt_acme_invoice_reconciler', {
      version_tag: '1.2.0',
      system_prompt: 'You are an autonomous invoice reconciliation agent.',
      tools: ['tool_erp_lookup', 'tool_ocr_extract'],
    });
    setScan(res);
    setScanning(false);
  };

  useEffect(() => {
    runScan();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <ShieldAlert className="w-7 h-7 text-indigo-400" />
            Agent Security Scanner & Risk Review
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Prompt injection resistance, tool permission boundaries, PII/PHI leakage detection, and CVE vulnerability scanning.
          </p>
        </div>
        <Button variant="intelligence" onClick={runScan} disabled={scanning}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${scanning ? 'animate-spin' : ''}`} /> Run Security Scan
          </span>
        </Button>
      </div>

      {scan && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="bg-slate-900/80 border-slate-800 lg:col-span-1">
            <CardHeader>
              <CardTitle className="text-base text-white">Security Scorecard</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-center">
              <div className="p-6 bg-slate-950 rounded-full w-32 h-32 mx-auto flex flex-col items-center justify-center border-4 border-emerald-500">
                <span className="text-3xl font-extrabold text-white">{scan.security_score}</span>
                <span className="text-[10px] text-slate-400 uppercase">Score / 100</span>
              </div>
              <Badge variant={scan.risk_level === 'LOW' ? 'success' : 'warning'} className="text-xs px-3 py-1">
                Risk Level: {scan.risk_level}
              </Badge>
              <div className="text-xs text-slate-400 text-left space-y-2 pt-3 border-t border-slate-800">
                <div className="flex justify-between">
                  <span>Prompt Injection Resistance:</span>
                  <span className="font-bold text-white">{scan.prompt_injection_resistance_pct}%</span>
                </div>
                <div className="flex justify-between">
                  <span>PII Leakage Detected:</span>
                  <span className="font-bold text-emerald-400">None</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/80 border-slate-800 lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-base text-white flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-amber-400" /> Vulnerability & Privilege Findings
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {scan.vulnerabilities.map((v) => (
                <div
                  key={v.vuln_id}
                  className="p-4 bg-slate-800/40 rounded-lg border border-slate-700/50 space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-semibold text-white">{v.category}</span>
                    <Badge variant={v.severity === 'CRITICAL' ? 'error' : 'warning'}>{v.severity}</Badge>
                  </div>
                  <p className="text-xs text-slate-300">{v.description}</p>
                  <p className="text-xs text-cyan-400 font-medium">Recommendation: {v.recommendation}</p>
                </div>
              ))}
              {scan.vulnerabilities.length === 0 && (
                <div className="p-8 text-center text-slate-400 flex items-center justify-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" /> No security vulnerabilities found.
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
