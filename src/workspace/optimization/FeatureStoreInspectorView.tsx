import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

interface FeatureItem {
  name: string;
  category: string;
  dataType: string;
  minBound: number;
  maxBound: number;
  currentValue: number;
  normalizedValue: number;
  normalizationType: string;
  driftScore: number;
  unit: string;
  description: string;
}

export const FeatureStoreInspectorView: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const features: FeatureItem[] = [
    {
      name: 'ocr_confidence',
      category: 'QUALITY',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1.0,
      currentValue: 0.942,
      normalizedValue: 0.942,
      normalizationType: 'IDENTITY',
      driftScore: 0.012,
      unit: 'prob',
      description: 'Raw confidence score from vision & OCR models',
    },
    {
      name: 'schema_validation_score',
      category: 'QUALITY',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1.0,
      currentValue: 1.0,
      normalizedValue: 1.0,
      normalizationType: 'IDENTITY',
      driftScore: 0.005,
      unit: 'ratio',
      description: 'Proportion of extracted fields passing strict schema validation',
    },
    {
      name: 'latency_p95_ms',
      category: 'PERFORMANCE',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 60000.0,
      currentValue: 840.0,
      normalizedValue: 0.014,
      normalizationType: 'MIN_MAX',
      driftScore: 0.021,
      unit: 'ms',
      description: 'Historical p95 execution latency in milliseconds',
    },
    {
      name: 'historical_success_rate',
      category: 'PERFORMANCE',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1.0,
      currentValue: 0.985,
      normalizedValue: 0.985,
      normalizationType: 'IDENTITY',
      driftScore: 0.008,
      unit: 'prob',
      description: 'Empirical success rate across historical document executions',
    },
    {
      name: 'retry_count',
      category: 'TELEMETRY',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 10.0,
      currentValue: 0.0,
      normalizedValue: 0.0,
      normalizationType: 'MIN_MAX',
      driftScore: 0.0,
      unit: 'count',
      description: 'Total number of execution retries on active task',
    },
    {
      name: 'memory_similarity',
      category: 'QUALITY',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1.0,
      currentValue: 0.884,
      normalizedValue: 0.884,
      normalizationType: 'IDENTITY',
      driftScore: 0.018,
      unit: 'similarity',
      description: 'Vector cosine similarity against episodic and semantic memory graph',
    },
    {
      name: 'document_complexity',
      category: 'QUALITY',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1.0,
      currentValue: 0.42,
      normalizedValue: 0.42,
      normalizationType: 'IDENTITY',
      driftScore: 0.034,
      unit: 'index',
      description: 'Structural and tabular complexity score of source document',
    },
    {
      name: 'worker_reliability',
      category: 'PERFORMANCE',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1.0,
      currentValue: 0.992,
      normalizedValue: 0.992,
      normalizationType: 'IDENTITY',
      driftScore: 0.002,
      unit: 'prob',
      description: 'Assigned worker agent historical reliability and uptime',
    },
    {
      name: 'gpu_load',
      category: 'RESOURCE',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1.0,
      currentValue: 0.31,
      normalizedValue: 0.31,
      normalizationType: 'IDENTITY',
      driftScore: 0.045,
      unit: 'ratio',
      description: 'Current normalized hardware GPU load factor',
    },
    {
      name: 'queue_length',
      category: 'RESOURCE',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1000.0,
      currentValue: 4.0,
      normalizedValue: 0.23,
      normalizationType: 'LOG',
      driftScore: 0.012,
      unit: 'count',
      description: 'Backlogged task count in worker priority queue',
    },
    {
      name: 'api_cost_usd',
      category: 'COST',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 10.0,
      currentValue: 0.0034,
      normalizedValue: 0.00034,
      normalizationType: 'MIN_MAX',
      driftScore: 0.001,
      unit: 'usd',
      description: 'Direct AI provider invocation cost in USD',
    },
    {
      name: 'token_count',
      category: 'RESOURCE',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 200000.0,
      currentValue: 2450.0,
      normalizedValue: 0.64,
      normalizationType: 'LOG',
      driftScore: 0.022,
      unit: 'tokens',
      description: 'Total token consumption for prompt and completion',
    },
    {
      name: 'human_validation_rate',
      category: 'QUALITY',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1.0,
      currentValue: 0.988,
      normalizedValue: 0.988,
      normalizationType: 'IDENTITY',
      driftScore: 0.004,
      unit: 'prob',
      description: 'Approval frequency during human-in-the-loop review',
    },
    {
      name: 'compliance_flags',
      category: 'COMPLIANCE',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 5.0,
      currentValue: 0.0,
      normalizedValue: 0.0,
      normalizationType: 'MIN_MAX',
      driftScore: 0.0,
      unit: 'count',
      description: 'Active regulatory, PII, or data residency alerts',
    },
    {
      name: 'anomaly_score',
      category: 'UNCERTAINTY',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1.0,
      currentValue: 0.038,
      normalizedValue: 0.038,
      normalizationType: 'IDENTITY',
      driftScore: 0.009,
      unit: 'score',
      description: 'Multidimensional statistical outlier metric',
    },
    {
      name: 'epistemic_uncertainty',
      category: 'UNCERTAINTY',
      dataType: 'float',
      minBound: 0.0,
      maxBound: 1.0,
      currentValue: 0.082,
      normalizedValue: 0.082,
      normalizationType: 'IDENTITY',
      driftScore: 0.015,
      unit: 'uncertainty',
      description: 'Model ignorance and out-of-distribution domain gap',
    },
  ];

  const filteredFeatures = features.filter((f) => {
    const matchesCat = selectedCategory === 'ALL' || f.category === selectedCategory;
    const matchesSearch = f.name.toLowerCase().includes(searchQuery.toLowerCase()) || f.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🗄️</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Scientific Feature Store & Schema Registry
              </h2>
              <Badge variant="success" size="sm">
                IMMUTABLE V1.4.0
              </Badge>
            </div>
            <p className="text-xs text-[#94A3B8] mt-1">
              Zero raw telemetry consumed directly by planners. 16 canonical features normalized, validated, and SHA-256 fingerprinted.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-right">
              <div className="text-xs font-mono text-[#94A3B8]">Schema Signature</div>
              <div className="text-xs font-mono text-cyan-400 font-bold">SHA-256: 8a4f9d2c...</div>
            </div>
          </div>
        </div>

        {/* Filter Controls */}
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-[#1E293B]">
          <div className="flex items-center gap-2 overflow-x-auto">
            {['ALL', 'QUALITY', 'PERFORMANCE', 'RESOURCE', 'COST', 'COMPLIANCE', 'UNCERTAINTY'].map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
                  selectedCategory === cat
                    ? 'bg-cyan-500 text-white shadow-[0_0_10px_rgba(6,182,212,0.4)]'
                    : 'bg-[#131D35] text-[#94A3B8] hover:text-[#F8FAFC]'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
          <input
            type="text"
            placeholder="Search feature parameters..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="bg-[#131D35] border border-[#334155] rounded-xl px-3 py-1.5 text-xs text-[#F8FAFC] placeholder-[#64748B] focus:outline-none focus:border-cyan-400 w-64"
          />
        </div>
      </div>

      {/* Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {filteredFeatures.map((f) => (
          <Card key={f.name} className="p-4 bg-[#0F172A]/90 border border-[#1E293B] hover:border-cyan-500/50 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs font-bold font-mono text-cyan-400 truncate">{f.name}</span>
                <Badge variant="outline" size="sm">
                  {f.category}
                </Badge>
              </div>
              <p className="text-[11px] text-[#94A3B8] mt-2 line-clamp-2 leading-relaxed">{f.description}</p>
            </div>

            <div className="mt-4 space-y-2 pt-3 border-t border-[#1E293B]/60">
              <div className="flex justify-between items-center text-xs">
                <span className="text-[#64748B]">Raw Value</span>
                <span className="font-mono font-bold text-[#F8FAFC]">
                  {f.currentValue} <span className="text-[#64748B] text-[10px]">{f.unit}</span>
                </span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-[#64748B]">Normalized [0, 1]</span>
                <span className="font-mono text-emerald-400 font-semibold">{f.normalizedValue.toFixed(4)}</span>
              </div>
              <div className="w-full bg-[#131D35] rounded-full h-1.5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-cyan-500 to-emerald-400 h-1.5 rounded-full"
                  style={{ width: `${Math.min(100, Math.max(2, f.normalizedValue * 100))}%` }}
                />
              </div>
              <div className="flex justify-between items-center text-[10px] text-[#64748B] pt-1">
                <span>Norm: {f.normalizationType}</span>
                <span className="text-cyan-400/80">Drift: {f.driftScore}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
