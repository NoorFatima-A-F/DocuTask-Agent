import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import {
  MessageSquare,
  Lock,
  ArrowRight,
  Clock,
} from 'lucide-react';

interface SwarmMessageItem {
  id: string;
  sender: string;
  recipient: string;
  type: 'DIRECT' | 'BROADCAST' | 'MULTICAST' | 'PUBLISH_SUBSCRIBE' | 'REQUEST_RESPONSE';
  topic: string;
  payloadSummary: string;
  signature: string;
  timestamp: string;
}

export const CommunicationMonitor: React.FC = () => {
  const [selectedType, setSelectedType] = useState<string>('ALL');
  const [selectedMsg, setSelectedMsg] = useState<SwarmMessageItem | null>(null);

  const messages: SwarmMessageItem[] = [
    {
      id: 'msg-001',
      sender: 'agent-exec-01',
      recipient: 'agent-plan-01',
      type: 'DIRECT',
      topic: 'mission_decomposition',
      payloadSummary: 'Decompose batch invoice mission into 4 parallel OCR stages with $120 budget constraint.',
      signature: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      timestamp: '14:22:01.104',
    },
    {
      id: 'msg-002',
      sender: 'agent-plan-01',
      recipient: 'ALL_SPECIALISTS',
      type: 'BROADCAST',
      topic: 'task_auction_announcement',
      payloadSummary: 'Published OCR extraction task (task_ocr_batch_01) on Task Marketplace.',
      signature: 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb',
      timestamp: '14:22:01.350',
    },
    {
      id: 'msg-003',
      sender: 'agent-spec-ocr',
      recipient: 'agent-plan-01',
      type: 'REQUEST_RESPONSE',
      topic: 'task_bid_submission',
      payloadSummary: 'Bid submitted: Cost $85.00, estimated latency 140ms, SLA adherence 99.9%.',
      signature: '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce',
      timestamp: '14:22:01.620',
    },
    {
      id: 'msg-004',
      sender: 'agent-coord-01',
      recipient: 'coalition-alpha',
      type: 'MULTICAST',
      topic: 'consensus_invitation',
      payloadSummary: 'Initiate weighted consensus voting on schema validation invariants for Mission 9482.',
      signature: '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
      timestamp: '14:22:01.910',
    },
    {
      id: 'msg-005',
      sender: 'agent-val-sec',
      recipient: 'agent-coord-01',
      type: 'DIRECT',
      topic: 'consensus_vote_cast',
      payloadSummary: 'Vote cast: APPROVE (Weight: 1.0, Confidence: 0.99) with cryptographic proof.',
      signature: 'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d',
      timestamp: '14:22:02.140',
    },
  ];

  const filteredMessages = messages.filter(m => selectedType === 'ALL' || m.type === selectedType);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Communication Bus Monitor</h1>
            <Badge variant="success" size="sm" hasDot isPulsing>
              BUS ONLINE
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time multi-agent communication traces, cryptographic message signatures, and selective context exchange.
          </p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-wrap gap-2">
        {['ALL', 'DIRECT', 'BROADCAST', 'MULTICAST', 'REQUEST_RESPONSE'].map(t => (
          <Button
            key={t}
            variant={selectedType === t ? 'primary' : 'outline'}
            size="sm"
            onClick={() => setSelectedType(t)}
          >
            {t}
          </Button>
        ))}
      </div>

      {/* Messages & Detail Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Message Stream */}
        <div className="lg:col-span-2 space-y-3">
          {filteredMessages.map(m => (
            <Card
              key={m.id}
              onClick={() => setSelectedMsg(m)}
              className={`p-4 cursor-pointer transition-all border ${
                selectedMsg?.id === m.id
                  ? 'border-primary ring-1 ring-primary bg-primary/5'
                  : 'border-border/60 hover:border-border'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Badge variant="outline" size="sm" className="font-mono">
                    {m.type}
                  </Badge>
                  <span className="text-xs font-semibold font-mono text-primary">#{m.topic}</span>
                </div>
                <div className="flex items-center gap-1.5 text-[11px] font-mono text-muted-foreground">
                  <Clock className="w-3 h-3" />
                  {m.timestamp}
                </div>
              </div>

              <div className="flex items-center gap-2 my-2 text-xs font-mono">
                <span className="font-bold text-foreground">{m.sender}</span>
                <ArrowRight className="w-3 h-3 text-muted-foreground" />
                <span className="font-bold text-foreground">{m.recipient}</span>
              </div>

              <p className="text-xs text-muted-foreground line-clamp-2">{m.payloadSummary}</p>
            </Card>
          ))}
        </div>

        {/* Selected Message Inspector */}
        <div>
          {selectedMsg ? (
            <Card className="p-5 border-border/60 sticky top-4 space-y-4">
              <div className="flex items-center justify-between border-b border-border/40 pb-3">
                <div>
                  <span className="text-[11px] font-mono text-muted-foreground block">Message ID</span>
                  <span className="font-bold text-xs font-mono">{selectedMsg.id}</span>
                </div>
                <Badge variant="success" size="sm">VERIFIED</Badge>
              </div>

              <div>
                <span className="text-xs font-semibold text-muted-foreground block mb-1">Payload Content</span>
                <div className="p-3 rounded bg-muted/20 border border-border/30 text-xs font-mono text-foreground leading-relaxed">
                  {selectedMsg.payloadSummary}
                </div>
              </div>

              <div>
                <span className="text-xs font-semibold text-muted-foreground flex items-center gap-1 mb-1">
                  <Lock className="w-3 h-3 text-primary" /> Ed25519 Cryptographic Signature
                </span>
                <div className="p-2 rounded bg-muted/30 border border-border/30 text-[10px] font-mono text-muted-foreground break-all">
                  {selectedMsg.signature}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="p-2 rounded bg-muted/10 border border-border/20">
                  <span className="text-[10px] text-muted-foreground block">Sender</span>
                  <span className="font-mono font-semibold">{selectedMsg.sender}</span>
                </div>
                <div className="p-2 rounded bg-muted/10 border border-border/20">
                  <span className="text-[10px] text-muted-foreground block">Recipient</span>
                  <span className="font-mono font-semibold">{selectedMsg.recipient}</span>
                </div>
              </div>
            </Card>
          ) : (
            <Card className="p-8 border-border/40 text-center text-muted-foreground">
              <MessageSquare className="w-8 h-8 mx-auto mb-2 opacity-40" />
              <p className="text-xs">Select a message packet from the stream to verify cryptographic signatures and context pointers.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
