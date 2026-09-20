import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { SSOProviderConfig, UserIdentity } from '../../types/saasPlatform';
import { KeyRound, ShieldCheck, Users, RefreshCw } from 'lucide-react';

export const IdentitySSOCenter: React.FC = () => {
  const [ssoList, setSsoList] = useState<SSOProviderConfig[]>([]);
  const [users, setUsers] = useState<UserIdentity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const [sso, u] = await Promise.all([
        SaaSApiClient.listSSOConfigs('tenant_acme_corp'),
        SaaSApiClient.listUsers('tenant_acme_corp'),
      ]);
      setSsoList(sso);
      setUsers(u);
      setLoading(false);
    };
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <KeyRound className="w-7 h-7 text-indigo-400" />
            Enterprise Identity & SSO Control
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Configure SAML 2.0, OIDC identity federations, SCIM 2.0 user sync, and MFA enforcement.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* SSO Config Card */}
        <Card className="bg-slate-900/80 border-slate-800 lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-base text-white flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-emerald-400" /> SSO Identity Provider
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {ssoList.map((sso) => (
              <div key={sso.provider_id} className="p-4 bg-slate-800/60 rounded border border-slate-700/60 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold text-white">{sso.name}</span>
                  <Badge variant="success">ACTIVE</Badge>
                </div>
                <div className="text-xs text-slate-400 space-y-1">
                  <div>Protocol: <span className="text-slate-200 font-mono">{sso.protocol}</span></div>
                  <div>Issuer: <span className="text-slate-200 truncate block font-mono">{sso.issuer_url}</span></div>
                  <div>Endpoint: <span className="text-slate-200 truncate block font-mono">{sso.sso_endpoint}</span></div>
                  <div>Fingerprint: <span className="text-cyan-400 font-mono text-[10px] block truncate">{sso.certificate_fingerprint}</span></div>
                </div>
              </div>
            ))}
            <Button variant="outline" className="w-full">
              <span className="flex items-center justify-center gap-2">
                <RefreshCw className="w-4 h-4" /> Trigger SCIM Directory Sync
              </span>
            </Button>
          </CardContent>
        </Card>

        {/* Users Table */}
        <Card className="bg-slate-900/80 border-slate-800 lg:col-span-2">
          <CardHeader>
            <CardTitle className="text-base text-white flex items-center gap-2">
              <Users className="w-5 h-5 text-indigo-400" /> Provisioned Enterprise Directory ({users.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="p-8 text-center text-slate-400">Loading directory...</div>
            ) : (
              <div className="space-y-3">
                {users.map((u) => (
                  <div
                    key={u.user_id}
                    className="p-3 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between"
                  >
                    <div>
                      <span className="text-sm font-semibold text-white block">{u.display_name}</span>
                      <span className="text-xs text-slate-400">{u.email} • {u.department}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <Badge variant="intelligence">{u.role}</Badge>
                      <Badge variant={u.mfa_enabled ? 'success' : 'warning'}>
                        {u.mfa_enabled ? 'MFA Enabled' : 'No MFA'}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
