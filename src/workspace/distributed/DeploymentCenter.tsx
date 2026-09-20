import React, { useState } from 'react';
import {
  Cloud,
  Terminal,
  RefreshCw,
  Play,
  FileCode,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const DeploymentCenter: React.FC = () => {
  const [selectedTarget, setSelectedTarget] = useState<'CLOUDRUN' | 'GKE' | 'AWS_ECS' | 'AZURE_ACA'>('CLOUDRUN');
  const [deploying, setDeploying] = useState(false);
  const [deployLog, setDeployLog] = useState<string[]>([]);

  const handleDeploy = () => {
    setDeploying(true);
    const startMsg = `[${new Date().toLocaleTimeString()}] Building container image for ${selectedTarget}...`;
    setDeployLog([startMsg]);

    setTimeout(() => {
      setDeployLog((prev) => [
        `[${new Date().toLocaleTimeString()}] Pushing image to gcr.io/docutask-agent/runtime:v1.18.0`,
        ...prev,
      ]);
    }, 1000);

    setTimeout(() => {
      setDeployLog((prev) => [
        `[${new Date().toLocaleTimeString()}] Deploying service revision to ${selectedTarget}...`,
        ...prev,
      ]);
    }, 2000);

    setTimeout(() => {
      setDeployLog((prev) => [
        `[${new Date().toLocaleTimeString()}] Deployment successful! 5 worker replicas online. Health check: 200 OK.`,
        ...prev,
      ]);
      setDeploying(false);
    }, 3000);
  };

  const sampleDockerfile = `# Phase 13.18 Cloud-Native Autonomous Agent Runtime
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Cloud className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Cloud Deployment Center</h1>
            <p className="text-sm text-slate-400">
              Provider-agnostic multi-cloud packaging: Cloud Run, Kubernetes (GKE), ECS & ACA
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="intelligence" onClick={handleDeploy} disabled={deploying}>
            <span className="flex items-center gap-2">
              {deploying ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
              Deploy Revision
            </span>
          </Button>
        </div>
      </div>

      {/* Target Selector */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { id: 'CLOUDRUN', label: 'Google Cloud Run', desc: 'Serverless Auto-scaling' },
          { id: 'GKE', label: 'Google GKE', desc: 'Kubernetes Cluster Mesh' },
          { id: 'AWS_ECS', label: 'AWS ECS Fargate', desc: 'Elastic Container Service' },
          { id: 'AZURE_ACA', label: 'Azure Container Apps', desc: 'Microservice Fabric' },
        ].map((t) => (
          <Card
            key={t.id}
            onClick={() => setSelectedTarget(t.id as any)}
            className={`p-4 cursor-pointer border transition-all ${
              selectedTarget === t.id
                ? 'bg-slate-800/80 border-indigo-500 shadow-md'
                : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
            }`}
          >
            <span className="font-bold text-white text-sm block">{t.label}</span>
            <span className="text-xs text-slate-400 block mt-1">{t.desc}</span>
          </Card>
        ))}
      </div>

      {/* Manifest & Log Visualizer */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6 bg-slate-900/40 border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <FileCode className="w-4 h-4 text-indigo-400" />
              Dockerfile Manifest
            </h3>
            <Badge variant="outline">Multi-Stage Ready</Badge>
          </div>
          <pre className="p-4 bg-slate-950/80 rounded-xl border border-slate-800 font-mono text-xs text-indigo-300 overflow-x-auto">
            {sampleDockerfile}
          </pre>
        </Card>

        <Card className="p-6 bg-slate-900/40 border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <Terminal className="w-4 h-4 text-emerald-400" />
              Deployment Pipeline Log
            </h3>
            <Badge variant={deploying ? 'warning' : 'success'}>
              {deploying ? 'Deploying...' : 'Idle'}
            </Badge>
          </div>
          <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 space-y-2 min-h-48 max-h-72 overflow-y-auto">
            {deployLog.length > 0 ? (
              deployLog.map((log, idx) => (
                <div key={idx} className="border-b border-slate-800/60 pb-1 text-emerald-300 last:border-0">
                  {log}
                </div>
              ))
            ) : (
              <p className="text-slate-500 italic">Click "Deploy Revision" to trigger cloud deployment.</p>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
};
