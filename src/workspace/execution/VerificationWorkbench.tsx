import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  FileCheck2,
  RotateCw,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { VerificationCertificate } from '../../types/executionPlatform';

export const VerificationWorkbench: React.FC = () => {
  const [certificates, setCertificates] = useState<VerificationCertificate[]>([]);
  const [selectedCert, setSelectedCert] = useState<VerificationCertificate | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadCertificates = async () => {
    try {
      setLoading(true);
      const res = await executionPlatformApiClient.listVerifications();
      setCertificates(res.certificates || []);
      if (res.certificates && res.certificates.length > 0 && !selectedCert) {
        setSelectedCert(res.certificates[0] || null);
      }
    } catch (err) {
      console.error('Failed to load certificates:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCertificates();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <FileCheck2 className="w-5 h-5 text-cyan-400" />
            Verification Workbench & Cryptographic Proofs
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Post-execution state invariant assertions, external API/DB diff verification & SHA-256 signatures
          </p>
        </div>
        <Button variant="outline" onClick={loadCertificates}>
          <span className="flex items-center gap-2">
            <RotateCw className="w-4 h-4" />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Certificate List */}
        <Card className="lg:col-span-1 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-white">
              Issued Proofs ({certificates.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 max-h-[600px] overflow-y-auto">
            {loading && certificates.length === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">Loading certificates...</p>
            ) : certificates.map((c) => (
              <div
                key={c.certificate_id}
                onClick={() => setSelectedCert(c)}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  selectedCert?.certificate_id === c.certificate_id
                    ? 'bg-purple-950/40 border-purple-600'
                    : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-cyan-300">{c.certificate_id}</span>
                  <Badge variant={c.passed ? 'success' : 'error'}>
                    {c.passed ? 'VERIFIED' : 'FAILED'}
                  </Badge>
                </div>
                <p className="text-[11px] text-slate-300 mt-1 font-mono">Tool: {c.tool_id}</p>
                <span className="text-[10px] text-slate-500 block truncate mt-1">
                  SHA: {c.state_signature_sha256.slice(0, 20)}...
                </span>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Right: Certificate Deep Inspector */}
        <Card className="lg:col-span-2 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base text-white">
                {selectedCert ? `Certificate ${selectedCert.certificate_id}` : 'Select a Certificate'}
              </CardTitle>
              {selectedCert && (
                <Badge variant="outline" className="font-mono text-xs text-cyan-400">
                  {selectedCert.mission_id}
                </Badge>
              )}
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {selectedCert && (
              <>
                {/* Cryptographic Proof Hash Banner */}
                <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                  <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block">
                    Cryptographic SHA-256 State Signature
                  </span>
                  <p className="text-xs font-mono text-cyan-300 break-all select-all">
                    {selectedCert.state_signature_sha256}
                  </p>
                </div>

                {/* Checks Table */}
                <div>
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Verified State Invariant Checks
                  </h4>
                  <div className="space-y-3">
                    {selectedCert.checks.map((chk) => (
                      <div
                        key={chk.check_id}
                        className="p-3 bg-slate-800/40 border border-slate-700/60 rounded-xl space-y-1.5"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-semibold text-white">{chk.name}</span>
                          <Badge variant={chk.passed ? 'success' : 'error'}>Passed</Badge>
                        </div>
                        <p className="text-xs text-slate-400 font-mono">
                          Target: <span className="text-slate-200">{chk.target_resource}</span>
                        </p>
                        <p className="text-xs text-emerald-400 font-mono">
                          Actual: {chk.actual_condition}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
