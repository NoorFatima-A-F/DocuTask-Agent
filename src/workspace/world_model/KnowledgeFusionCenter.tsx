/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 2: Knowledge Fusion Center
 */

import React, { useEffect, useState } from 'react';
import {
  Brain,
  Sparkles,
  RefreshCw,
  Plus,
  ShieldCheck,
  Search,
  Clock,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
import { FusedFact } from '../../types/worldModelPlatform';

export const KnowledgeFusionCenter: React.FC = () => {
  const [facts, setFacts] = useState<FusedFact[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [subject, setSubject] = useState('');
  const [predicate, setPredicate] = useState('');
  const [objectVal, setObjectVal] = useState('');
  const [fusing, setFusing] = useState(false);

  const fetchFacts = async () => {
    setLoading(true);
    try {
      const res = await WorldModelApiClient.getFacts();
      setFacts(res.facts || []);
    } catch (err) {
      console.error('Error fetching facts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFacts();
  }, []);

  const handleFuseFact = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!subject || !predicate || !objectVal) return;
    setFusing(true);
    try {
      await WorldModelApiClient.fuseFact({
        subject,
        predicate,
        object: objectVal,
        confidence: 0.95,
        source: 'knowledge_fusion_center_ui',
      });
      setSubject('');
      setPredicate('');
      setObjectVal('');
      setShowAddModal(false);
      await fetchFacts();
    } catch (err) {
      console.error('Error fusing fact:', err);
    } finally {
      setFusing(false);
    }
  };

  const filtered = facts.filter(
    (f) =>
      f.subject.toLowerCase().includes(search.toLowerCase()) ||
      f.predicate.toLowerCase().includes(search.toLowerCase()) ||
      String(f.object).toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-cyan-500/30 rounded-xl p-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/30 rounded-lg text-cyan-400">
            <Brain className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-white tracking-tight">Knowledge Fusion Center</h1>
              <Badge variant="intelligence">Epistemic Truth Ranking</Badge>
            </div>
            <p className="text-sm text-slate-400">
              Integrates multi-runtime facts, resolves conflicting evidence, and tracks exponential decay freshness.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={fetchFacts} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={() => setShowAddModal(true)}>
            <span className="flex items-center gap-2">
              <Plus className="w-4 h-4" />
              Fuse New Fact
            </span>
          </Button>
        </div>
      </div>

      {/* Search & Stats Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search subjects, predicates, objects..."
            className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>

        <div className="flex items-center gap-4 text-xs text-slate-400">
          <div>Total Facts: <span className="font-bold text-white">{facts.length}</span></div>
          <div>Average Truth Score: <span className="font-bold text-cyan-400">97.8%</span></div>
          <div>Confidence Threshold: <span className="font-bold text-emerald-400">&gt;0.85</span></div>
        </div>
      </div>

      {/* Facts Table/Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((fact) => (
          <Card key={fact.fact_id} className="bg-slate-900/60 border-slate-800 p-4 hover:border-cyan-500/40 transition-all space-y-3">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-500/30">
                  {fact.fact_id}
                </span>
                <Badge variant="success">Truth: {Math.round((fact.truth_score || 0.95) * 100)}%</Badge>
              </div>
              <div className="flex items-center gap-1 text-[11px] text-slate-400">
                <Clock className="w-3.5 h-3.5" />
                <span>{new Date(fact.last_reinforced_at || fact.created_at).toLocaleTimeString()}</span>
              </div>
            </div>

            {/* RDF Triple representation */}
            <div className="p-3 bg-slate-950/80 rounded-lg border border-slate-800 font-mono text-xs space-y-1.5">
              <div className="flex items-center gap-2">
                <span className="text-slate-400 font-sans text-[11px] w-16">Subject:</span>
                <span className="text-white font-semibold">{fact.subject}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-slate-400 font-sans text-[11px] w-16">Predicate:</span>
                <span className="text-cyan-300">{fact.predicate}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-slate-400 font-sans text-[11px] w-16">Object:</span>
                <span className="text-emerald-300 font-medium">{String(fact.object)}</span>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
              <div className="flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Source: <strong className="text-slate-300">{fact.source}</strong></span>
              </div>
              <div>
                Verifications: <strong className="text-slate-300">{fact.verification_count || 1}</strong>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Add Fact Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="bg-slate-900 border-slate-700 w-full max-w-lg p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-cyan-400" />
                Fuse New Knowledge Fact
              </h3>
              <button onClick={() => setShowAddModal(false)} className="text-slate-400 hover:text-white">✕</button>
            </div>

            <form onSubmit={handleFuseFact} className="space-y-4 text-sm">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Subject Entity</label>
                <input
                  type="text"
                  required
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="e.g. DocumentOCRWorkerPool"
                  className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white focus:outline-none focus:border-cyan-500 text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Predicate / Relation</label>
                <input
                  type="text"
                  required
                  value={predicate}
                  onChange={(e) => setPredicate(e.target.value)}
                  placeholder="e.g. degradesThroughputWhenMemoryExceeds"
                  className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white focus:outline-none focus:border-cyan-500 text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Object Value / Target</label>
                <input
                  type="text"
                  required
                  value={objectVal}
                  onChange={(e) => setObjectVal(e.target.value)}
                  placeholder="e.g. 85%"
                  className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white focus:outline-none focus:border-cyan-500 text-sm"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3">
                <Button variant="outline" type="button" onClick={() => setShowAddModal(false)}>
                  Cancel
                </Button>
                <Button variant="intelligence" type="submit" disabled={fusing}>
                  {fusing ? 'Fusing...' : 'Fuse Fact'}
                </Button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
};
