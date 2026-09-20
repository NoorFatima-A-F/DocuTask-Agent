import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { Tenant, PlanTier } from '../../types/saasPlatform';
import { Building2, Plus, Shield, Globe, Cpu, RefreshCw, CheckCircle2 } from 'lucide-react';

export const TenantManagementCenter: React.FC = () => {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({
    tenant_id: '',
    company_name: '',
    slug: '',
    admin_email: '',
    tier: 'ENTERPRISE' as PlanTier,
  });

  const loadTenants = async () => {
    setLoading(true);
    const list = await SaaSApiClient.listTenants();
    setTenants(list);
    setLoading(false);
  };

  useEffect(() => {
    loadTenants();
  }, []);

  const handleOnboard = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.tenant_id || !form.company_name) return;
    await SaaSApiClient.onboardTenant(form);
    setShowModal(false);
    loadTenants();
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Building2 className="w-7 h-7 text-indigo-400" />
            Tenant Fleet Management
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Provision, isolate, configure limits, and govern enterprise customer accounts.
          </p>
        </div>
        <Button variant="intelligence" onClick={() => setShowModal(true)}>
          <span className="flex items-center gap-2">
            <Plus className="w-4 h-4" /> Provision New Tenant
          </span>
        </Button>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Tenant Fleet...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {tenants.map((t) => (
            <Card key={t.tenant_id} className="bg-slate-900/80 border-slate-800">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-lg text-white">{t.company_name}</CardTitle>
                    <span className="text-xs font-mono text-slate-400">{t.tenant_id}</span>
                  </div>
                  <Badge variant={t.tier === 'ENTERPRISE' ? 'intelligence' : 'info'}>{t.tier}</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-3 text-xs bg-slate-800/40 p-3 rounded border border-slate-700/50">
                  <div>
                    <span className="text-slate-400 block">Status</span>
                    <Badge variant={t.status === 'ACTIVE' ? 'success' : 'warning'} className="mt-1">
                      {t.status}
                    </Badge>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Admin Contact</span>
                    <span className="text-slate-200 font-medium truncate block mt-1">{t.admin_email}</span>
                  </div>
                </div>

                {/* Resource Limits */}
                <div className="space-y-2">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                    <Cpu className="w-3.5 h-3.5 text-indigo-400" /> Resource Limits & Quotas
                  </span>
                  <div className="grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="bg-slate-800/60 p-2 rounded">
                      <span className="text-slate-400 block text-[10px]">Workspaces</span>
                      <span className="font-bold text-white">{t.limits.max_workspaces}</span>
                    </div>
                    <div className="bg-slate-800/60 p-2 rounded">
                      <span className="text-slate-400 block text-[10px]">Concurrent Agents</span>
                      <span className="font-bold text-white">{t.limits.max_concurrent_agents}</span>
                    </div>
                    <div className="bg-slate-800/60 p-2 rounded">
                      <span className="text-slate-400 block text-[10px]">Budget Cap</span>
                      <span className="font-bold text-emerald-400">${t.limits.monthly_budget_ceiling_usd.toLocaleString()}</span>
                    </div>
                  </div>
                </div>

                {/* Config Badges */}
                <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-800">
                  {t.config.enforce_sso && (
                    <Badge variant="sentinel" className="text-[10px] flex items-center gap-1">
                      <Shield className="w-3 h-3" /> SSO Enforced
                    </Badge>
                  )}
                  {t.config.custom_domain && (
                    <Badge variant="outline" className="text-[10px] flex items-center gap-1">
                      <Globe className="w-3 h-3" /> {t.config.custom_domain}
                    </Badge>
                  )}
                  <Badge variant="outline" className="text-[10px]">
                    Region: {t.config.default_region}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Onboarding Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <Card className="bg-slate-900 border-slate-700 max-w-md w-full shadow-2xl">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-indigo-400" /> Provision Enterprise Tenant
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleOnboard} className="space-y-4">
                <div>
                  <label className="text-xs text-slate-300 font-medium block mb-1">Tenant ID (Identifier)</label>
                  <input
                    type="text"
                    required
                    placeholder="tenant_cyberdyne_systems"
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-indigo-500"
                    value={form.tenant_id}
                    onChange={(e) => setForm({ ...form, tenant_id: e.target.value })}
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-300 font-medium block mb-1">Company / Organization Name</label>
                  <input
                    type="text"
                    required
                    placeholder="Cyberdyne Systems Corp"
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-indigo-500"
                    value={form.company_name}
                    onChange={(e) => setForm({ ...form, company_name: e.target.value })}
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-300 font-medium block mb-1">Slug</label>
                  <input
                    type="text"
                    required
                    placeholder="cyberdyne-systems"
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-indigo-500"
                    value={form.slug}
                    onChange={(e) => setForm({ ...form, slug: e.target.value })}
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-300 font-medium block mb-1">Admin Email</label>
                  <input
                    type="email"
                    required
                    placeholder="admin@cyberdyne.com"
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-indigo-500"
                    value={form.admin_email}
                    onChange={(e) => setForm({ ...form, admin_email: e.target.value })}
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-300 font-medium block mb-1">Plan Tier</label>
                  <select
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-indigo-500"
                    value={form.tier}
                    onChange={(e) => setForm({ ...form, tier: e.target.value as PlanTier })}
                  >
                    <option value="PRO">PRO ($499/mo)</option>
                    <option value="BUSINESS">BUSINESS ($2,499/mo)</option>
                    <option value="ENTERPRISE">ENTERPRISE ($7,999/mo)</option>
                  </select>
                </div>
                <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
                  <Button variant="ghost" type="button" onClick={() => setShowModal(false)}>
                    Cancel
                  </Button>
                  <Button variant="intelligence" type="submit">
                    <span className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4" /> Deploy Stack
                    </span>
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
