import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Zap,
  Search,
  RotateCw,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { ToolDefinition } from '../../types/executionPlatform';

export const ToolRegistryExplorer: React.FC = () => {
  const [tools, setTools] = useState<ToolDefinition[]>([]);
  const [selectedTool, setSelectedTool] = useState<ToolDefinition | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  const loadTools = async () => {
    try {
      setLoading(true);
      const res = await executionPlatformApiClient.listTools({
        category: categoryFilter || undefined,
        search: searchQuery || undefined,
      });
      setTools(res.tools || []);
      if (res.tools && res.tools.length > 0 && !selectedTool) {
        setSelectedTool(res.tools[0] || null);
      }
    } catch (err) {
      console.error('Failed to load tools:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTools();
  }, [categoryFilter]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadTools();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-400" />
            Universal Tool Registry & Capability Taxonomy
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Dynamic discovery, JSON Schema contract validation, latency tracking & compensation bindings
          </p>
        </div>
        <Button variant="outline" onClick={loadTools}>
          <span className="flex items-center gap-2">
            <RotateCw className="w-4 h-4" />
            Refresh
          </span>
        </Button>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row gap-3">
        <form onSubmit={handleSearchSubmit} className="flex-1 flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
            <input
              type="text"
              className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-white text-sm focus:outline-none focus:border-purple-500"
              placeholder="Search tools by name, tag or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <Button variant="secondary" onClick={loadTools}>Search</Button>
        </form>
        <select
          className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-purple-500"
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
        >
          <option value="">All Categories</option>
          <option value="code_repository">Code Repositories (GitHub)</option>
          <option value="communication">Communication (Slack)</option>
          <option value="infrastructure">Infrastructure (K8s)</option>
          <option value="cloud">Cloud (AWS/GCP)</option>
          <option value="database">Database (PostgreSQL)</option>
          <option value="payment_finance">Payment & Finance (Stripe)</option>
          <option value="browser_vision">Browser Vision (Playwright)</option>
        </select>
      </div>

      {/* Main Grid: Tool List & Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-white">Registered Tools ({tools.length})</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 max-h-[600px] overflow-y-auto">
            {loading && tools.length === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">Loading tools...</p>
            ) : tools.map((t) => (
              <div
                key={t.tool_id}
                onClick={() => setSelectedTool(t)}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  selectedTool?.tool_id === t.tool_id
                    ? 'bg-purple-950/40 border-purple-600'
                    : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-white truncate max-w-[180px]">{t.name}</span>
                  <Badge variant="outline">{t.tool_type}</Badge>
                </div>
                <div className="flex items-center justify-between mt-2 text-[11px] text-slate-400">
                  <span className="text-amber-400">Health: {(t.health_score * 100).toFixed(0)}%</span>
                  <span>{t.average_latency_ms}ms avg</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Right: Tool Deep Inspector */}
        <Card className="lg:col-span-2 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base text-white">
                {selectedTool ? selectedTool.name : 'Select a Tool'}
              </CardTitle>
              {selectedTool && (
                <Badge
                  variant={
                    selectedTool.risk_level === 'low'
                      ? 'success'
                      : selectedTool.risk_level === 'medium'
                      ? 'warning'
                      : 'error'
                  }
                >
                  {selectedTool.risk_level.toUpperCase()} RISK
                </Badge>
              )}
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {selectedTool && (
              <>
                <p className="text-sm text-slate-300">{selectedTool.description}</p>

                {/* Telemetry Metrics */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-3 bg-slate-950/60 rounded-lg border border-slate-800 text-xs">
                  <div>
                    <span className="text-slate-500 block">Rate Limit</span>
                    <span className="text-slate-200 font-mono">{selectedTool.rate_limit_per_min} req/min</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Timeout</span>
                    <span className="text-slate-200 font-mono">{selectedTool.timeout_seconds}s</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Total Calls</span>
                    <span className="text-slate-200 font-mono">{selectedTool.total_calls}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Compensation Tool</span>
                    <span className="text-purple-300 font-mono truncate block">
                      {selectedTool.compensation_tool_id || 'None'}
                    </span>
                  </div>
                </div>

                {/* Parameters Schema Table */}
                <div>
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Input Parameters Specification
                  </h4>
                  <div className="border border-slate-800 rounded-lg overflow-hidden">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-slate-950 text-slate-400">
                        <tr>
                          <th className="p-2.5">Parameter</th>
                          <th className="p-2.5">Type</th>
                          <th className="p-2.5">Required</th>
                          <th className="p-2.5">Description</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800 text-slate-300">
                        {selectedTool.parameters.map((p) => (
                          <tr key={p.name} className="hover:bg-slate-800/30">
                            <td className="p-2.5 font-mono text-purple-300">{p.name}</td>
                            <td className="p-2.5 font-mono text-slate-400">{p.param_type}</td>
                            <td className="p-2.5">
                              {p.required ? (
                                <span className="text-red-400">Yes</span>
                              ) : (
                                <span className="text-slate-500">No</span>
                              )}
                            </td>
                            <td className="p-2.5 text-slate-400">{p.description}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
