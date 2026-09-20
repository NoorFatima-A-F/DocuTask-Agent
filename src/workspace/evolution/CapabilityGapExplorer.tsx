import React, { useState, useEffect } from 'react';
import {
  Search,
  Sparkles,
  PlusCircle,
  AlertCircle,
  RefreshCw,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { CapabilityDescriptorPayload } from '../../types/evolutionPlatform';

export const CapabilityGapExplorer: React.FC = () => {
  const [capabilities, setCapabilities] = useState<CapabilityDescriptorPayload[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [discovering, setDiscovering] = useState<boolean>(false);
  const [showRegisterModal, setShowRegisterModal] = useState<boolean>(false);

  // Form states
  const [name, setName] = useState<string>('');
  const [domain, setDomain] = useState<string>('document_intelligence');
  const [description, setDescription] = useState<string>('');
  const [maturity, setMaturity] = useState<string>('EXPERIMENTAL');

  useEffect(() => {
    loadCapabilities();
  }, []);

  const loadCapabilities = async () => {
    setLoading(true);
    try {
      const data = await EvolutionPlatformApiClient.listCapabilities();
      setCapabilities(data);
    } catch (err) {
      console.error('Failed to load capabilities:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDiscover = async () => {
    setDiscovering(true);
    try {
      const data = await EvolutionPlatformApiClient.discoverCapabilities();
      setCapabilities(data);
    } catch (err) {
      console.error('Error discovering capabilities:', err);
    } finally {
      setDiscovering(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    try {
      const newCap = await EvolutionPlatformApiClient.registerCapability({
        name,
        domain,
        description,
        maturity_level: maturity,
        accuracy_score: 0.96,
        latency_ms: 18.0,
        cost_per_invocation: 0.0012,
      });
      setCapabilities((prev) => [...prev, newCap]);
      setShowRegisterModal(false);
      setName('');
      setDescription('');
    } catch (err) {
      console.error('Registration failed:', err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-purple-500/10 border border-purple-500/20 rounded-xl">
            <Search className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Capability Gap & Architectural Discovery</h1>
              <Badge variant="intelligence" size="sm">Autonomous Detection</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Uncovers missing capabilities, redundant agent roles, knowledge blind spots, and synthesizes new modular descriptors.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={loadCapabilities}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button
            variant="outline"
            onClick={() => setShowRegisterModal(true)}
          >
            <span className="flex items-center gap-2">
              <PlusCircle className="w-4 h-4" />
              Register Capability
            </span>
          </Button>
          <Button
            variant="intelligence"
            onClick={handleDiscover}
            disabled={discovering}
          >
            <span className="flex items-center gap-2">
              <Sparkles className={`w-4 h-4 ${discovering ? 'animate-spin' : ''}`} />
              {discovering ? 'Scanning Platform...' : 'Discover Capability Gaps'}
            </span>
          </Button>
        </div>
      </div>

      {/* Grid of Capabilities */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {capabilities.map((cap) => (
          <div
            key={cap.capability_id}
            className={`bg-slate-900/80 border ${cap.is_gap ? 'border-amber-500/40' : 'border-slate-800'} rounded-xl p-5 space-y-4 hover:border-slate-700 transition-all flex flex-col justify-between`}
          >
            <div className="space-y-2">
              <div className="flex items-start justify-between gap-2">
                <span className="text-sm font-semibold text-slate-100 leading-snug">{cap.name}</span>
                <Badge
                  variant={cap.is_gap ? 'warning' : cap.state === 'ACTIVE' ? 'success' : 'outline'}
                  size="sm"
                >
                  {cap.is_gap ? 'Gap Discovered' : cap.state}
                </Badge>
              </div>
              <p className="text-xs text-slate-400">{cap.description || 'Core platform modular capability'}</p>
            </div>

            {cap.is_gap && (
              <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-200 flex items-start gap-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-amber-400" />
                <span>{cap.gap_rationale}</span>
              </div>
            )}

            <div className="pt-3 border-t border-slate-800/80 grid grid-cols-3 gap-2 text-center text-xs font-mono">
              <div className="bg-slate-950/60 p-2 rounded">
                <div className="text-slate-500 text-[10px]">EFFICIENCY</div>
                <div className="text-slate-200 font-semibold">{(cap.efficiency_score * 100).toFixed(0)}%</div>
              </div>
              <div className="bg-slate-950/60 p-2 rounded">
                <div className="text-slate-500 text-[10px]">LATENCY</div>
                <div className="text-indigo-300 font-semibold">{cap.latency_ms.toFixed(0)}ms</div>
              </div>
              <div className="bg-slate-950/60 p-2 rounded">
                <div className="text-slate-500 text-[10px]">ACCURACY</div>
                <div className="text-emerald-300 font-semibold">{(cap.accuracy_score * 100).toFixed(0)}%</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal for Registering Capability */}
      {showRegisterModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-lg w-full space-y-4 shadow-2xl">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-slate-100">Register Subsystem Capability</h3>
              <button
                onClick={() => setShowRegisterModal(false)}
                className="text-slate-400 hover:text-slate-200 text-sm font-semibold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleRegister} className="space-y-4">
              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">Capability Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Adaptive AST Layout Segmenter"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500 font-mono"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-medium text-slate-300 block mb-1">Domain</label>
                  <select
                    value={domain}
                    onChange={(e) => setDomain(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
                  >
                    <option value="document_intelligence">Document Intelligence</option>
                    <option value="caching">Caching & Memory</option>
                    <option value="orchestration">Swarm Orchestration</option>
                    <option value="governance">Security & Governance</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs font-medium text-slate-300 block mb-1">Maturity Level</label>
                  <select
                    value={maturity}
                    onChange={(e) => setMaturity(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
                  >
                    <option value="EXPERIMENTAL">EXPERIMENTAL</option>
                    <option value="VALIDATING">VALIDATING</option>
                    <option value="PRODUCTION">PRODUCTION</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">Description & Rationale</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Provide details on throughput, algorithm design, and purpose..."
                  rows={3}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
                />
              </div>

              <div className="flex justify-end gap-3 pt-2">
                <Button variant="ghost" onClick={() => setShowRegisterModal(false)}>
                  Cancel
                </Button>
                <Button variant="intelligence" type="submit">
                  Save Capability
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
