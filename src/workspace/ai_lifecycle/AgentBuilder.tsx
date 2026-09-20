import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import type { AgentTemplate, AgentCategory } from '../../types/aiLifecycle';
import { Wrench, CheckCircle2, Sparkles, Code2, Bot, RefreshCw } from 'lucide-react';

export const AgentBuilder: React.FC = () => {
  const [templates, setTemplates] = useState<AgentTemplate[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<AgentTemplate | null>(null);
  const [form, setForm] = useState({
    name: '',
    slug: '',
    category: 'AUTOMATION' as AgentCategory,
    system_prompt: '',
    tools: 'tool_erp_lookup, tool_ocr_extract',
    owner_email: 'admin@acmecorp.com',
  });
  const [submitting, setSubmitting] = useState(false);
  const [releasedAgent, setReleasedAgent] = useState<any>(null);

  useEffect(() => {
    const load = async () => {
      const list = await AILifecycleApiClient.listTemplates();
      setTemplates(list);
      if (list.length > 0 && list[0]) {
        applyTemplate(list[0]);
      }
    };
    load();
  }, []);

  const applyTemplate = (t: AgentTemplate) => {
    setSelectedTemplate(t);
    setForm({
      name: t.name,
      slug: t.name.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
      category: t.category,
      system_prompt: t.default_prompt,
      tools: t.default_tools.join(', '),
      owner_email: 'admin@acmecorp.com',
    });
  };

  const handleBuildAndDeploy = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    const toolsArray = form.tools.split(',').map((t) => t.trim()).filter(Boolean);
    const res = await fetch('/api/v1/ai-lifecycle/full-release', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tenant_id: 'tenant_acme_corp',
        organization_id: 'org_acme_americas',
        workspace_id: 'ws_acme_invoicing',
        name: form.name,
        slug: form.slug,
        category: form.category,
        owner_id: 'usr_acme_admin',
        owner_email: form.owner_email,
        system_prompt: form.system_prompt,
        tools: toolsArray,
        connectors: ['conn_acme_sap'],
      }),
    });
    if (res.ok) {
      const data = await res.json();
      setReleasedAgent(data);
    }
    setSubmitting(false);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Wrench className="w-7 h-7 text-indigo-400" />
            AI Application Builder & Starter Studio
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Scaffold, configure prompts, bind tools, and trigger turnkey CI/CD release pipelines.
          </p>
        </div>
      </div>

      {/* Starter Templates */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {templates.map((tmpl) => (
          <div
            key={tmpl.template_id}
            onClick={() => applyTemplate(tmpl)}
            className={`p-4 rounded-xl border cursor-pointer transition ${
              selectedTemplate?.template_id === tmpl.template_id
                ? 'bg-indigo-950/40 border-indigo-500 shadow-lg'
                : 'bg-slate-900/80 border-slate-800 hover:border-slate-700'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <Badge variant="intelligence">{tmpl.category}</Badge>
              <Sparkles className="w-4 h-4 text-indigo-400" />
            </div>
            <span className="text-sm font-semibold text-white block">{tmpl.name}</span>
            <p className="text-xs text-slate-400 mt-1 line-clamp-2">{tmpl.description}</p>
          </div>
        ))}
      </div>

      {/* Builder Form */}
      <Card className="bg-slate-900/80 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white flex items-center gap-2">
            <Code2 className="w-5 h-5 text-emerald-400" /> Agent Configuration & CI/CD Release
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleBuildAndDeploy} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-slate-300 font-medium block mb-1">Application Name</label>
                <input
                  type="text"
                  required
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-indigo-500"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
              <div>
                <label className="text-xs text-slate-300 font-medium block mb-1">Category</label>
                <select
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-indigo-500"
                  value={form.category}
                  onChange={(e) => setForm({ ...form, category: e.target.value as AgentCategory })}
                >
                  <option value="FINANCIAL_AUDIT">FINANCIAL_AUDIT</option>
                  <option value="COMPLIANCE">COMPLIANCE</option>
                  <option value="LEGAL_ANALYSIS">LEGAL_ANALYSIS</option>
                  <option value="AUTOMATION">AUTOMATION</option>
                  <option value="EXTRACTION">EXTRACTION</option>
                  <option value="RESEARCH">RESEARCH</option>
                </select>
              </div>
            </div>

            <div>
              <label className="text-xs text-slate-300 font-medium block mb-1">System Prompt Directives</label>
              <textarea
                rows={4}
                required
                className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white font-mono focus:outline-none focus:border-indigo-500"
                value={form.system_prompt}
                onChange={(e) => setForm({ ...form, system_prompt: e.target.value })}
              />
            </div>

            <div>
              <label className="text-xs text-slate-300 font-medium block mb-1">Bound Tools (Comma separated)</label>
              <input
                type="text"
                className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white font-mono"
                value={form.tools}
                onChange={(e) => setForm({ ...form, tools: e.target.value })}
              />
            </div>

            <div className="flex justify-end pt-3 border-t border-slate-800">
              <Button variant="intelligence" type="submit" disabled={submitting}>
                <span className="flex items-center gap-2">
                  {submitting ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Bot className="w-4 h-4" />}
                  Execute DevSecOps Release Pipeline
                </span>
              </Button>
            </div>
          </form>

          {releasedAgent && (
            <div className="mt-6 p-4 rounded-lg bg-emerald-950/30 border border-emerald-800/50 space-y-2">
              <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
                <CheckCircle2 className="w-5 h-5" /> Full Lifecycle Release Successful!
              </div>
              <div className="text-xs text-slate-300 grid grid-cols-2 gap-2 font-mono">
                <div>Agent ID: {releasedAgent.agent.agent_id}</div>
                <div>State: {releasedAgent.agent.lifecycle_state}</div>
                <div>Test Quality Score: {releasedAgent.test_result.accuracy_score}</div>
                <div>Security Score: {releasedAgent.security_scan.security_score}/100</div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
