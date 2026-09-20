import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { TenantPolicy } from '../../types/saasPlatform';
import { Scale, Lock, RefreshCw } from 'lucide-react';

export const PolicyAdministrationCenter: React.FC = () => {
  const [policies, setPolicies] = useState<TenantPolicy[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const list = await SaaSApiClient.listPolicies('tenant_acme_corp');
      setPolicies(list);
      setLoading(false);
    };
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Scale className="w-7 h-7 text-indigo-400" />
            Tenant Policy & RBAC/ABAC Engine
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Fine-grained authorization, geo-fencing constraints, role bindings, and spend cap rules.
          </p>
        </div>
      </div>

      <Card className="bg-slate-900/80 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white flex items-center gap-2">
            <Lock className="w-4 h-4 text-cyan-400" /> Active Authorization Policies ({policies.length})
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {loading ? (
            <div className="p-8 text-center text-slate-400">
              <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading policies...
            </div>
          ) : (
            policies.map((p) => (
              <div
                key={p.policy_id}
                className="p-4 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-white">{p.policy_name}</span>
                    <Badge variant={p.effect === 'ALLOW' ? 'success' : 'error'}>{p.effect}</Badge>
                  </div>
                  <span className="text-xs text-slate-400 block mt-1">
                    Role: <span className="text-slate-200 font-mono">{p.subject_role}</span> • Resource: <span className="text-slate-200 font-mono">{p.resource_type}</span> • Action: <span className="text-slate-200 font-mono">{p.action}</span>
                  </span>
                </div>
                <div className="text-right text-xs text-slate-500 font-mono">
                  {p.policy_id}
                </div>
              </div>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  );
};
