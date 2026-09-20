import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { TaskMarketplaceListing } from '../../types/workforce';
import { ShoppingCart, DollarSign, Clock, Gavel, Plus } from 'lucide-react';

export const TaskMarketplace: React.FC = () => {
  const [tasks, setTasks] = useState<TaskMarketplaceListing[]>([]);
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [budget, setBudget] = useState('30');

  useEffect(() => {
    workforceApiClient.getMarketplaceTasks().then(setTasks);
  }, []);

  const handlePost = async () => {
    if (!title || !desc) return;
    const newTask = await workforceApiClient.postTask({
      title,
      description: desc,
      required_skills: ['Document Extraction'],
      budget_max_usd: parseFloat(budget) || 30.0
    });
    setTasks([...tasks, newTask]);
    setTitle('');
    setDesc('');
  };

  const handleAssign = async (taskId: string) => {
    const updated = await workforceApiClient.submitBid({
      task_id: taskId,
      employee_id: 'emp-doc-spec-01',
      bid_cost_usd: 12.0,
      estimated_duration_minutes: 10.0,
      solution_outline: 'Automated Stream Sharding'
    });
    setTasks(tasks.map(t => t.id === taskId ? updated : t));
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <span className="p-2 bg-amber-500/20 text-amber-400 rounded-xl">🛒</span>
          Task Marketplace & Internal Economy
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Autonomous Agent Job Bidding, Auction Mechanisms, and Value Optimization
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="p-5 bg-slate-900/50 border-slate-800 lg:col-span-1">
          <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <Plus className="w-4 h-4 text-emerald-400" /> Post Work Request
          </h3>
          <div className="space-y-3">
            <div>
              <label className="text-xs text-slate-400 block mb-1">Task Title</label>
              <input
                placeholder="e.g. Audit Ledger Line Items"
                value={title}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)}
                className="bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full"
              />
            </div>
            <div>
              <label className="text-xs text-slate-400 block mb-1">Task Description</label>
              <input
                placeholder="Details on required accuracy and inputs"
                value={desc}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setDesc(e.target.value)}
                className="bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full"
              />
            </div>
            <div>
              <label className="text-xs text-slate-400 block mb-1">Max Budget (USD)</label>
              <input
                placeholder="30"
                value={budget}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setBudget(e.target.value)}
                className="bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full"
              />
            </div>
            <Button className="w-full mt-2" onClick={handlePost}>
              <span className="flex items-center gap-2">
                <ShoppingCart className="w-4 h-4" /> Publish to Marketplace
              </span>
            </Button>
          </div>
        </Card>

        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Gavel className="w-4 h-4 text-indigo-400" /> Active Bidding Auctions
          </h3>
          <div className="space-y-4">
            {tasks.map((t) => (
              <Card key={t.id} className="p-5 bg-slate-900/50 border-slate-800">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <div className="text-base font-bold text-white">{t.title}</div>
                    <div className="text-xs text-slate-400 mt-0.5">{t.description}</div>
                  </div>
                  <Badge variant={t.status === 'OPEN' ? 'default' : 'outline'}>{t.status}</Badge>
                </div>

                <div className="flex gap-4 my-3 text-xs text-slate-400">
                  <span className="flex items-center gap-1">
                    <DollarSign className="w-3.5 h-3.5 text-emerald-400" /> Max Budget: ${t.budget_max_usd}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-blue-400" /> Priority: {t.priority}
                  </span>
                  <span>Bids: <strong>{t.bids.length}</strong></span>
                </div>

                {t.bids.length > 0 && (
                  <div className="my-3 space-y-2">
                    <div className="text-[11px] font-semibold text-slate-400 uppercase">Current Leading Bids</div>
                    {t.bids.map((b) => (
                      <div key={b.bid_id} className="p-2.5 bg-slate-950/60 rounded-lg border border-slate-800 flex justify-between items-center text-xs">
                        <div>
                          <strong className="text-indigo-400">{b.employee_id}</strong>: ${b.bid_cost_usd} in {b.estimated_duration_minutes}m
                          <div className="text-[10px] text-slate-500">{b.proposed_solution_outline}</div>
                        </div>
                        <Badge variant="outline">{Math.round(b.confidence_score * 100)}% Conf</Badge>
                      </div>
                    ))}
                  </div>
                )}

                <div className="pt-2 flex justify-end">
                  <Button size="sm" variant="outline" onClick={() => handleAssign(t.id)}>
                    <span className="flex items-center gap-1">
                      <Gavel className="w-3.5 h-3.5" /> Submit Agent Bid
                    </span>
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
