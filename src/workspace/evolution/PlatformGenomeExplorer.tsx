import React, { useState, useEffect } from 'react';
import {
  Dna,
  RefreshCw,
  Copy,
  Check,
  Code2,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { PlatformGenomePayload } from '../../types/evolutionPlatform';

export const PlatformGenomeExplorer: React.FC = () => {
  const [genome, setGenome] = useState<PlatformGenomePayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [copied, setCopied] = useState<boolean>(false);

  useEffect(() => {
    loadGenome();
  }, []);

  const loadGenome = async () => {
    setLoading(true);
    try {
      const data = await EvolutionPlatformApiClient.getPlatformGenome();
      setGenome(data);
    } catch (err) {
      console.error('Failed to load platform genome:', err);
    } finally {
      setLoading(false);
    }
  };

  const copyJson = () => {
    if (!genome) return;
    navigator.clipboard.writeText(JSON.stringify(genome, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-purple-500/10 border border-purple-500/20 rounded-xl">
            <Dna className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Platform Architecture Genome Explorer</h1>
              <Badge variant="intelligence" size="sm">Blueprint Specification</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Inspect the comprehensive genome configuration, active hyperparameters, modular subsystems, and immutable rollback manifests.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={loadGenome}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button
            variant="outline"
            onClick={copyJson}
          >
            <span className="flex items-center gap-2">
              {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              {copied ? 'Copied Genome' : 'Export Genome JSON'}
            </span>
          </Button>
        </div>
      </div>

      {/* Genome Details JSON & Visualizer */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-semibold text-slate-100">Genome Manifest</h2>
          <div className="space-y-3 text-xs font-mono text-slate-300">
            <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1">
              <div className="text-slate-500 text-[10px]">GENOME ID</div>
              <div className="text-purple-300 font-bold">{genome?.genome_id ?? 'genome_v13_13_prime'}</div>
            </div>
            <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1">
              <div className="text-slate-500 text-[10px]">ACTIVE PLATFORM VERSION</div>
              <div className="text-emerald-300 font-bold">{genome?.version ?? 'v13.13.0'}</div>
            </div>
            <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1">
              <div className="text-slate-500 text-[10px]">TIMESTAMP</div>
              <div className="text-slate-300">{genome?.timestamp ?? new Date().toISOString()}</div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center gap-2">
            <Code2 className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-semibold text-slate-100">Genome JSON Inspector</h2>
          </div>
          <pre className="bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-300 overflow-x-auto max-h-[460px] leading-relaxed">
            {genome ? JSON.stringify(genome, null, 2) : 'Loading Platform Genome...'}
          </pre>
        </div>
      </div>
    </div>
  );
};
