import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { BrandingConfig } from '../../types/saasPlatform';
import { Palette, Globe, Mail, Eye, RefreshCw } from 'lucide-react';

export const WhiteLabelStudio: React.FC = () => {
  const [branding, setBranding] = useState<BrandingConfig | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const data = await SaaSApiClient.getBranding('tenant_acme_corp');
      setBranding(data);
      setLoading(false);
    };
    load();
  }, []);

  if (loading || !branding) {
    return (
      <div className="p-12 text-center text-slate-400">
        <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading White-Label Studio...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Palette className="w-7 h-7 text-indigo-400" />
            White-Label & Custom Branding Studio
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Configure custom CNAME domains, corporate themes, logos, and branded customer portals.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="bg-slate-900/80 border-slate-800">
          <CardHeader>
            <CardTitle className="text-base text-white">Brand Configuration</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-xs text-slate-400 block mb-1">Brand Name</label>
              <input
                type="text"
                className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white"
                value={branding.brand_name}
                readOnly
              />
            </div>

            <div>
              <label className="text-xs text-slate-400 block mb-1">Custom CNAME Domain</label>
              <div className="flex items-center gap-2">
                <Globe className="w-4 h-4 text-indigo-400" />
                <input
                  type="text"
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white font-mono"
                  value={branding.custom_cname_domain || 'ai.acmecorp.com'}
                  readOnly
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-slate-400 block mb-1">Primary Color</label>
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded border border-slate-600" style={{ backgroundColor: branding.primary_color_hex }}></div>
                  <span className="text-sm text-white font-mono">{branding.primary_color_hex}</span>
                </div>
              </div>
              <div>
                <label className="text-xs text-slate-400 block mb-1">Secondary Color</label>
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded border border-slate-600" style={{ backgroundColor: branding.secondary_color_hex }}></div>
                  <span className="text-sm text-white font-mono">{branding.secondary_color_hex}</span>
                </div>
              </div>
            </div>

            <div>
              <label className="text-xs text-slate-400 block mb-1">Support Email</label>
              <div className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-slate-400" />
                <input
                  type="text"
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white"
                  value={branding.support_email}
                  readOnly
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Live Preview Card */}
        <Card className="bg-slate-900/80 border-slate-800">
          <CardHeader>
            <CardTitle className="text-base text-white flex items-center gap-2">
              <Eye className="w-4 h-4 text-cyan-400" /> Live Tenant Portal Preview
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-6 rounded-xl bg-slate-950 border border-slate-800 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded-full" style={{ backgroundColor: branding.primary_color_hex }}></div>
                  <span className="font-bold text-white text-sm">{branding.brand_name}</span>
                </div>
                <Badge variant="outline" className="text-[10px]">{branding.custom_cname_domain}</Badge>
              </div>

              <div className="p-4 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-xs text-slate-400 block">Welcome to your enterprise workspace</span>
                <span className="text-lg font-bold text-white mt-1 block">Autonomous Document Operations</span>
                <Button variant="intelligence" className="mt-3 text-xs">
                  Launch Mission
                </Button>
              </div>

              <div className="text-[10px] text-slate-500 text-center pt-2">
                {branding.email_footer_text}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
