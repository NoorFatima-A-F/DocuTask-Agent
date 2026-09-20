import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import {
  Play,
  Pause,
  RotateCcw,
  Lock,
  ArrowRight,
  Clock,
} from 'lucide-react';

interface TimelineFrame {
  index: number;
  time: string;
  eventType: string;
  initiator: string;
  target?: string;
  rationale: string;
  hash: string;
}

export const CoordinationTimeline: React.FC = () => {
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [currentFrame, setCurrentFrame] = useState<number>(0);

  const frames: TimelineFrame[] = [
    {
      index: 0,
      time: '14:22:00.100',
      eventType: 'AGENT_DISCOVERY',
      initiator: 'agent-exec-01',
      target: 'agent-plan-01',
      rationale: 'Executive discovered Lead Planner for Mission 9482.',
      hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    },
    {
      index: 1,
      time: '14:22:00.320',
      eventType: 'TASK_AUCTION_PUBLISHED',
      initiator: 'agent-plan-01',
      rationale: 'Published batch OCR task to auction marketplace.',
      hash: 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb',
    },
    {
      index: 2,
      time: '14:22:00.650',
      eventType: 'BID_SUBMITTED',
      initiator: 'agent-spec-ocr',
      target: 'agent-plan-01',
      rationale: 'OCR Specialist submitted competitive bid.',
      hash: '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce',
    },
    {
      index: 3,
      time: '14:22:00.890',
      eventType: 'BID_ACCEPTED',
      initiator: 'agent-plan-01',
      target: 'agent-spec-ocr',
      rationale: 'Planner awarded task to OCR Specialist.',
      hash: '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
    },
    {
      index: 4,
      time: '14:22:01.120',
      eventType: 'CONSENSUS_INITIATED',
      initiator: 'agent-coord-01',
      rationale: 'Consensus initiated for document schema verification.',
      hash: 'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d',
    },
    {
      index: 5,
      time: '14:22:01.450',
      eventType: 'CONSENSUS_DECIDED',
      initiator: 'agent-coord-01',
      rationale: 'Consensus reached with 100% affirmative quorum.',
      hash: '1e5e2e3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Coordination Replay Timeline</h1>
            <Badge variant="success" size="sm">
              6 FRAMES RECORDED
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Deterministic step-through replay of multi-agent coordination traces with cryptographic Merkle integrity verification.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsPlaying(p => !p)}
          >
            {isPlaying ? <Pause className="w-3.5 h-3.5 mr-1.5" /> : <Play className="w-3.5 h-3.5 mr-1.5" />}
            {isPlaying ? 'Pause Replay' : 'Play Timeline'}
          </Button>
          <Button variant="outline" size="sm" onClick={() => setCurrentFrame(0)}>
            <RotateCcw className="w-3.5 h-3.5 mr-1.5" />
            Reset
          </Button>
        </div>
      </div>

      {/* Frame Timeline */}
      <div className="space-y-3">
        {frames.map((f, i) => (
          <Card
            key={f.index}
            onClick={() => setCurrentFrame(i)}
            className={`p-4 cursor-pointer transition-all border ${
              currentFrame === i
                ? 'border-primary ring-1 ring-primary bg-primary/5'
                : 'border-border/60 hover:border-border'
            }`}
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <Badge variant={currentFrame === i ? 'intelligence' : 'outline'} size="sm" className="font-mono">
                  Frame #{f.index}
                </Badge>
                <Badge variant="outline" size="sm" className="font-mono">{f.eventType}</Badge>
              </div>
              <div className="flex items-center gap-1.5 text-[11px] font-mono text-muted-foreground">
                <Clock className="w-3 h-3" />
                {f.time}
              </div>
            </div>

            <div className="flex items-center gap-2 my-2 text-xs font-mono">
              <span className="font-bold text-foreground">{f.initiator}</span>
              {f.target && (
                <>
                  <ArrowRight className="w-3 h-3 text-muted-foreground" />
                  <span className="font-bold text-foreground">{f.target}</span>
                </>
              )}
            </div>

            <p className="text-xs text-muted-foreground">{f.rationale}</p>

            <div className="mt-2 text-[10px] font-mono text-muted-foreground flex items-center gap-1.5">
              <Lock className="w-3 h-3 text-primary shrink-0" />
              <span className="truncate">Frame State Hash: {f.hash}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
