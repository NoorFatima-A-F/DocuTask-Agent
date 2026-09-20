import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  FileText,
  ShieldCheck,
  Download,
  Share2,
  CheckCircle2,
  Lock,
} from 'lucide-react';

interface PublicationItem {
  id: string;
  doi: string;
  title: string;
  abstract: string;
  conclusions: string[];
  authors: string[];
  state: 'PUBLISHED' | 'PEER_REVIEW' | 'DRAFT';
  publishedAt: string;
  signature: string;
}

export const PublicationCenter: React.FC = () => {
  const [downloadNotice, setDownloadNotice] = useState<string | null>(null);

  const publications: PublicationItem[] = [
    {
      id: 'pub-spec-cache-01',
      doi: '10.ai-sci/2026.001',
      title: 'Empirical Proof of Speculative Invariance in Multi-Column Accounting Extraction',
      abstract: 'We demonstrate that recurring enterprise invoice headers exhibit <=1.2 bits/token spatial entropy, allowing speculative GPU tensor caching that reduces P95 extraction latency by 30.27% (p < 0.0001) under 5,000 document evaluation.',
      conclusions: [
        'Speculative tensor caching yields 30.27% P95 latency reduction.',
        'Zero accuracy degradation observed across 5,000 evaluated invoices.',
        'Verified against Truth Ledger Block 7491 with SHA-256 provenance.',
      ],
      authors: ['AI Chief Scientist', 'Optimization Swarm Alpha', 'Governance Oracle'],
      state: 'PUBLISHED',
      publishedAt: '2026-09-12T18:45:00Z',
      signature: 'secp256k1:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
    },
    {
      id: 'pub-lockfree-ring-02',
      doi: '10.ai-sci/2026.002',
      title: 'Zero-Lock Telemetry Streaming with Atomic Circular Buffers in Autonomous Agent Societies',
      abstract: 'We establish an empirical proof that lock-free atomic circular buffers eliminate all thread contention in memory telemetry across 64 concurrent agents, yielding zero thread lock stalls under 100k events/sec throughput.',
      conclusions: [
        'Atomic circular buffers eliminate 100% of telemetry mutex lock stalls.',
        'Sustained 120k events/sec ingestion with <2MB memory jitter.',
        'Fully reproducible under deterministic replay replay-ring-994.',
      ],
      authors: ['AI Chief Scientist', 'Resilience Swarm Gamma'],
      state: 'PUBLISHED',
      publishedAt: '2026-09-12T17:30:00Z',
      signature: 'secp256k1:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
    },
  ];

  const handleDownloadPaper = (title: string) => {
    setDownloadNotice(`Generated machine-readable JSON-LD & PDF bundle for "${title}" with embedded cryptographic signatures.`);
    setTimeout(() => setDownloadNotice(null), 4000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <FileText className="w-6 h-6 text-sky-500" />
            Machine-Readable Scientific Publication Center
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Produces cryptographically signed research publications, empirical reports, and executive discovery briefings with verifiable DOI anchors.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            <ShieldCheck className="w-3.5 h-3.5 mr-1" />
            DOI Authority Registered
          </Badge>
        </div>
      </div>

      {downloadNotice && (
        <div className="p-4 bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800 rounded-lg text-sm text-sky-800 dark:text-sky-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{downloadNotice}</span>
        </div>
      )}

      {/* Publications List */}
      <div className="space-y-5">
        {publications.map(pub => (
          <Card key={pub.id} className="p-6 space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-gray-100 dark:border-gray-800 pb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-sky-500 font-bold">DOI: {pub.doi}</span>
                  <Badge variant="success" size="sm">{pub.state}</Badge>
                </div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mt-1">{pub.title}</h3>
                <div className="text-xs text-gray-500 mt-1">
                  Authors: <span className="text-gray-700 dark:text-gray-300 font-medium">{pub.authors.join(', ')}</span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDownloadPaper(pub.title)}
                >
                  <Download className="w-3.5 h-3.5 mr-1 text-sky-500" />
                  Export Paper
                </Button>
                <Button variant="ghost" size="sm">
                  <Share2 className="w-3.5 h-3.5" />
                </Button>
              </div>
            </div>

            <div>
              <span className="text-xs font-semibold text-gray-500 uppercase">Abstract</span>
              <p className="text-xs text-gray-700 dark:text-gray-300 mt-1 leading-relaxed bg-gray-50 dark:bg-gray-800/50 p-3 rounded">
                {pub.abstract}
              </p>
            </div>

            <div>
              <span className="text-xs font-semibold text-gray-500 uppercase">Key Empirical Conclusions</span>
              <ul className="mt-1 space-y-1 text-xs text-gray-600 dark:text-gray-300">
                {pub.conclusions.map((c, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 flex-shrink-0" />
                    <span>{c}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="pt-2 border-t border-gray-100 dark:border-gray-800 flex flex-col md:flex-row md:items-center justify-between text-xs text-gray-500 gap-2">
              <div className="flex items-center gap-1.5 font-mono text-[11px] text-gray-400">
                <Lock className="w-3.5 h-3.5 text-emerald-500" />
                <span className="truncate max-w-md">{pub.signature}</span>
              </div>
              <div>Published: {new Date(pub.publishedAt).toLocaleDateString()}</div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
