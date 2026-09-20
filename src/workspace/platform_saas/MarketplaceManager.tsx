import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { MarketplaceAsset } from '../../types/saasPlatform';
import { Store, Download, Star, RefreshCw, Check } from 'lucide-react';

export const MarketplaceManager: React.FC = () => {
  const [assets, setAssets] = useState<MarketplaceAsset[]>([]);
  const [installedMap, setInstalledMap] = useState<Record<string, boolean>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const list = await SaaSApiClient.listMarketplaceAssets();
      setAssets(list);
      setLoading(false);
    };
    load();
  }, []);

  const handleInstall = async (assetId: string) => {
    await SaaSApiClient.installAsset(assetId, 'tenant_acme_corp');
    setInstalledMap((prev) => ({ ...prev, [assetId]: true }));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Store className="w-7 h-7 text-indigo-400" />
            Enterprise AI Marketplace
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Discover, evaluate, and install verified Agent Packs, OCR Pipelines, and Workflow Templates.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Marketplace Assets...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {assets.map((asset) => {
            const isInstalled = installedMap[asset.asset_id];
            return (
              <Card key={asset.asset_id} className="bg-slate-900/80 border-slate-800 flex flex-col justify-between">
                <CardHeader>
                  <div className="flex items-center justify-between mb-1">
                    <Badge variant="intelligence">{asset.asset_type}</Badge>
                    <div className="flex items-center gap-1 text-amber-400 text-xs font-bold">
                      <Star className="w-3.5 h-3.5 fill-current" /> {asset.rating}
                    </div>
                  </div>
                  <CardTitle className="text-lg text-white">{asset.title}</CardTitle>
                  <span className="text-xs text-slate-400">Published by {asset.publisher_name} • v{asset.version}</span>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-xs text-slate-300 line-clamp-2">{asset.description}</p>
                  
                  <div className="flex flex-wrap gap-1.5">
                    {asset.tags.map((tag) => (
                      <span key={tag} className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">
                        #{tag}
                      </span>
                    ))}
                  </div>

                  <div className="flex items-center justify-between pt-3 border-t border-slate-800">
                    <div>
                      <span className="text-sm font-bold text-white">
                        {asset.price_monthly_usd === 0 ? 'Free' : `$${asset.price_monthly_usd}/mo`}
                      </span>
                      <span className="text-[10px] text-slate-400 block">{asset.downloads_count} installs</span>
                    </div>

                    <Button
                      variant={isInstalled ? 'secondary' : 'intelligence'}
                      disabled={isInstalled}
                      onClick={() => handleInstall(asset.asset_id)}
                    >
                      <span className="flex items-center gap-1.5 text-xs">
                        {isInstalled ? (
                          <>
                            <Check className="w-3.5 h-3.5 text-emerald-400" /> Installed
                          </>
                        ) : (
                          <>
                            <Download className="w-3.5 h-3.5" /> Install Pack
                          </>
                        )}
                      </span>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
