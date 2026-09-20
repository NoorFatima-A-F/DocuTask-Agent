import React from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import {
  History,
  CheckCircle2,
  FlaskConical,
  BookOpen,
  FileText,
  Compass,
} from 'lucide-react';

interface TimelineEvent {
  id: string;
  time: string;
  title: string;
  description: string;
  type: 'HYPOTHESIS' | 'EXPERIMENT' | 'VALIDATION' | 'LAW' | 'PUBLICATION';
}

export const DiscoveryTimeline: React.FC = () => {
  const events: TimelineEvent[] = [
    {
      id: 'evt-01',
      time: '18:45 UTC',
      title: 'Publication Signed & Registered with DOI',
      description: 'Official paper "Empirical Proof of Speculative Invariance in Multi-Column Accounting Extraction" published under DOI: 10.ai-sci/2026.001 with SHA-256 seal.',
      type: 'PUBLICATION',
    },
    {
      id: 'evt-02',
      time: '18:42 UTC',
      title: 'Consensus Tribunal Ratification',
      description: 'Multi-Agent Tribunal achieved 100% unanimous approval across Sentinel, Statistician, and Architect agents.',
      type: 'VALIDATION',
    },
    {
      id: 'evt-03',
      time: '18:40 UTC',
      title: 'Empirical Law Formulated',
      description: 'Ratified "Law of Speculative Invariance in Structured Documents" with governing equation Latency_P95(H, C).',
      type: 'LAW',
    },
    {
      id: 'evt-04',
      time: '18:35 UTC',
      title: 'A/B Experiment Completed (p < 0.0001)',
      description: 'A/B controlled trial exp-cache-ab-01 evaluated 2,500 document traces, confirming 30.27% extraction latency reduction with Cohen\'s d = 1.42.',
      type: 'EXPERIMENT',
    },
    {
      id: 'evt-05',
      time: '18:30 UTC',
      title: 'Hypothesis Formulated (EIG = 0.915)',
      description: 'Autonomous Knowledge Gap Scanner detected uncharacterized memory eviction and formulated Speculative Layout Cache hypothesis.',
      type: 'HYPOTHESIS',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <History className="w-6 h-6 text-indigo-500" />
            Autonomous Discovery Chronology & Provenance Timeline
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Chronological audit trail of all hypothesis formulations, experimental benchmarks, statistical validations, and ratified governing laws.
          </p>
        </div>
      </div>

      {/* Timeline Stream */}
      <Card className="p-6">
        <div className="relative border-l-2 border-indigo-200 dark:border-indigo-900 ml-4 space-y-6">
          {events.map(event => (
            <div key={event.id} className="relative pl-6">
              {/* Dot Icon */}
              <div className="absolute -left-3 top-0.5 w-6 h-6 rounded-full bg-white dark:bg-gray-800 border-2 border-indigo-500 flex items-center justify-center">
                {event.type === 'PUBLICATION' && <FileText className="w-3 h-3 text-sky-500" />}
                {event.type === 'VALIDATION' && <CheckCircle2 className="w-3 h-3 text-emerald-500" />}
                {event.type === 'LAW' && <BookOpen className="w-3 h-3 text-purple-500" />}
                {event.type === 'EXPERIMENT' && <FlaskConical className="w-3 h-3 text-amber-500" />}
                {event.type === 'HYPOTHESIS' && <Compass className="w-3 h-3 text-indigo-500" />}
              </div>

              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono text-gray-400">{event.time}</span>
                  <Badge variant="outline" size="sm">{event.type}</Badge>
                </div>
                <h4 className="text-sm font-semibold text-gray-900 dark:text-white">{event.title}</h4>
                <p className="text-xs text-gray-600 dark:text-gray-300">{event.description}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
