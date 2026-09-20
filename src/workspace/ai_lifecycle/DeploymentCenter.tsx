import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Rocket, Activity } from 'lucide-react';

export const DeploymentCenter: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Rocket className="w-7 h-7 text-indigo-400" />
            Distributed Deployment & Traffic Routing
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Blue-Green and Canary traffic orchestration across Phase 13.18 Distributed Cloud Runtime.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-slate-900/80 border-slate-800">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base text-white">Canary Release Strategy</CardTitle>
              <Badge variant="success">PRODUCTION (100%)</Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-4 bg-slate-950 rounded-lg border border-slate-800 space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300">Traffic Distribution</span>
                <span className="text-emerald-400 font-bold">100% Canary v1.2.0</span>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-500 h-2 w-full"></div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700/50">
                <span className="text-slate-400 block text-[10px]">Cluster ID</span>
                <span className="text-white font-mono font-medium">cluster_us_east_primary</span>
              </div>
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700/50">
                <span className="text-slate-400 block text-[10px]">Instances</span>
                <span className="text-cyan-400 font-bold font-mono">8 Active Workers</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/80 border-slate-800">
          <CardHeader>
            <CardTitle className="text-base text-white flex items-center gap-2">
              <Activity className="w-5 h-5 text-indigo-400" /> Runtime Health & Cluster Metrics
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              { label: 'Mean Response Latency', val: '310 ms', badge: 'success' },
              { label: 'Cluster Error Rate', val: '0.02%', badge: 'success' },
              { label: 'Distributed Queue Depth', val: '4 messages', badge: 'intelligence' },
            ].map((m, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-slate-800/40 rounded border border-slate-700/50">
                <span className="text-xs text-slate-300">{m.label}</span>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-white font-mono">{m.val}</span>
                  <Badge variant={m.badge as any}>HEALTHY</Badge>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
