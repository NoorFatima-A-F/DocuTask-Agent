import React, { useState, useEffect } from 'react';
import {
  Globe,
  MapPin,
  RefreshCw,
  ArrowRightLeft,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
import { RegionTopologyInfo } from '../../types/distributedPlatform';

export const MultiRegionFabricMap: React.FC = () => {
  const [regions, setRegions] = useState<RegionTopologyInfo[]>([]);
  const [loading, setLoading] = useState(true);

  const loadRegions = async () => {
    try {
      setLoading(true);
      const res = await DistributedApiClient.getRegions();
      setRegions(res);
    } catch (err) {
      console.error('Failed to load regions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRegions();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Globe className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Multi-Region Fabric Map</h1>
            <p className="text-sm text-slate-400">
              Global agent node topology, edge mesh routing, and inter-region latency matrices
            </p>
          </div>
        </div>

        <Button variant="outline" onClick={loadRegions} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh Topology
          </span>
        </Button>
      </div>

      {/* Regions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {regions.map((reg) => (
          <Card key={reg.region} className="p-5 bg-slate-900/40 border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-indigo-400" />
                <h3 className="font-bold text-white font-mono text-sm">{reg.region}</h3>
              </div>
              <Badge variant="success">{reg.status}</Badge>
            </div>

            <p className="text-xs text-slate-300 font-sans">{reg.location}</p>

            <div className="pt-2 border-t border-slate-800 flex justify-between items-center text-xs font-mono">
              <span className="text-slate-400">Intra-Region Latency:</span>
              <span className="text-emerald-400 font-bold">{reg.avg_latency_ms.toFixed(1)} ms</span>
            </div>
          </Card>
        ))}
      </div>

      {/* Latency Matrix Table */}
      <Card className="p-6 bg-slate-900/40 border-slate-800 space-y-4">
        <h3 className="text-base font-semibold text-white flex items-center gap-2">
          <ArrowRightLeft className="w-4 h-4 text-cyan-400" />
          Inter-Region Latency Matrix (Round-Trip ms)
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono text-slate-300">
            <thead className="bg-slate-800/60 uppercase text-slate-400 border-b border-slate-700">
              <tr>
                <th className="py-3 px-4">From / To</th>
                <th className="py-3 px-4">us-east-1</th>
                <th className="py-3 px-4">us-west-2</th>
                <th className="py-3 px-4">eu-central-1</th>
                <th className="py-3 px-4">asia-east-1</th>
                <th className="py-3 px-4">pk-south-1</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              <tr className="hover:bg-slate-800/30">
                <td className="py-3 px-4 font-bold text-white">us-east-1</td>
                <td className="py-3 px-4 text-emerald-400">8.5 ms</td>
                <td className="py-3 px-4 text-slate-300">65.0 ms</td>
                <td className="py-3 px-4 text-slate-300">85.0 ms</td>
                <td className="py-3 px-4 text-amber-400">180.0 ms</td>
                <td className="py-3 px-4 text-amber-400">210.0 ms</td>
              </tr>
              <tr className="hover:bg-slate-800/30">
                <td className="py-3 px-4 font-bold text-white">eu-central-1</td>
                <td className="py-3 px-4 text-slate-300">85.0 ms</td>
                <td className="py-3 px-4 text-slate-300">140.0 ms</td>
                <td className="py-3 px-4 text-emerald-400">10.2 ms</td>
                <td className="py-3 px-4 text-amber-400">190.0 ms</td>
                <td className="py-3 px-4 text-slate-300">115.0 ms</td>
              </tr>
              <tr className="hover:bg-slate-800/30">
                <td className="py-3 px-4 font-bold text-white">pk-south-1</td>
                <td className="py-3 px-4 text-amber-400">210.0 ms</td>
                <td className="py-3 px-4 text-amber-400">240.0 ms</td>
                <td className="py-3 px-4 text-slate-300">115.0 ms</td>
                <td className="py-3 px-4 text-slate-300">95.0 ms</td>
                <td className="py-3 px-4 text-emerald-400">6.0 ms</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
