import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import type { AgentMarketplaceListing } from '../../types/aiLifecycle';
import { Store, Star, Download, RefreshCw } from 'lucide-react';

export const MarketplaceStudio: React.FC = () => {
  const [listings, setListings] = useState<AgentMarketplaceListing[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const list = await AILifecycleApiClient.listMarketplaceListings();
      setListings(list);
      setLoading(false);
    };
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Store className="w-7 h-7 text-indigo-400" />
            Enterprise AI Application Marketplace Studio
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Enterprise-wide sharing, verified security certifications, community ratings, and one-click installs.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Marketplace...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {listings.map((l) => (
            <Card key={l.listing_id} className="bg-slate-900/80 border-slate-800 flex flex-col justify-between">
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="intelligence">{l.category}</Badge>
                  <div className="flex items-center gap-1 text-amber-400 text-xs font-bold">
                    <Star className="w-3.5 h-3.5 fill-current" /> {l.rating}
                  </div>
                </div>
                <CardTitle className="text-lg text-white">{l.title}</CardTitle>
                <span className="text-xs text-slate-400">By {l.publisher_name} • v{l.version}</span>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-xs text-slate-300">{l.description}</p>
                <div className="flex items-center justify-between pt-3 border-t border-slate-800">
                  <div>
                    <span className="text-sm font-bold text-white">
                      {l.price_monthly_usd === 0 ? 'Free' : `$${l.price_monthly_usd}/mo`}
                    </span>
                    <span className="text-[10px] text-slate-400 block">{l.install_count} installs</span>
                  </div>
                  <Button variant="intelligence">
                    <span className="flex items-center gap-1.5 text-xs">
                      <Download className="w-3.5 h-3.5" /> Install Application
                    </span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
