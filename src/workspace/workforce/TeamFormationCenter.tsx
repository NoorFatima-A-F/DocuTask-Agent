import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { DynamicTeam } from '../../types/workforce';
import { Users, Zap, Plus } from 'lucide-react';

export const TeamFormationCenter: React.FC = () => {
  const [teams, setTeams] = useState<DynamicTeam[]>([]);
  const [teamName, setTeamName] = useState('');
  const [mission, setMission] = useState('');
  const [skills, setSkills] = useState('');
  const [budget, setBudget] = useState('200');

  useEffect(() => {
    workforceApiClient.getTeams().then(setTeams);
  }, []);

  const handleFormTeam = async () => {
    if (!teamName || !mission) return;
    const reqSkills = skills.split(',').map(s => s.trim()).filter(Boolean);
    const newTeam = await workforceApiClient.formTeam({
      team_name: teamName,
      mission,
      required_skills: reqSkills.length ? reqSkills : ['Document Extraction', 'OCR Verification'],
      max_budget_usd: parseFloat(budget) || 200
    });
    setTeams([...teams, newTeam]);
    setTeamName('');
    setMission('');
    setSkills('');
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <span className="p-2 bg-purple-500/20 text-purple-400 rounded-xl">⚡</span>
          Dynamic Team Formation Center
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Constraint-Optimized Autonomous Multi-Agent Task Forces
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="p-5 bg-slate-900/50 border-slate-800 lg:col-span-1">
          <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-400" /> Assemble Task Force
          </h3>
          <div className="space-y-3">
            <div>
              <label className="text-xs text-slate-400 block mb-1">Team Name</label>
              <input
                placeholder="e.g. Audit Rapid Strike Force"
                value={teamName}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setTeamName(e.target.value)}
                className="bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full"
              />
            </div>
            <div>
              <label className="text-xs text-slate-400 block mb-1">Mission Objective</label>
              <input
                placeholder="e.g. Validate 5,000 PDF invoices with zero fabrication"
                value={mission}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setMission(e.target.value)}
                className="bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full"
              />
            </div>
            <div>
              <label className="text-xs text-slate-400 block mb-1">Required Skills (comma-separated)</label>
              <input
                placeholder="Document Extraction, OCR Verification"
                value={skills}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSkills(e.target.value)}
                className="bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full"
              />
            </div>
            <div>
              <label className="text-xs text-slate-400 block mb-1">Max Budget (USD)</label>
              <input
                placeholder="200"
                value={budget}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setBudget(e.target.value)}
                className="bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full"
              />
            </div>
            <Button className="w-full mt-2" onClick={handleFormTeam}>
              <span className="flex items-center gap-2">
                <Plus className="w-4 h-4" /> Form Autonomous Team
              </span>
            </Button>
          </div>
        </Card>

        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Users className="w-4 h-4 text-indigo-400" /> Active Dynamic Teams
          </h3>
          <div className="space-y-4">
            {teams.map((t) => (
              <Card key={t.id} className="p-5 bg-slate-900/50 border-slate-800">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <div className="text-base font-bold text-white">{t.team_name}</div>
                    <div className="text-xs text-slate-400 mt-0.5">{t.mission}</div>
                  </div>
                  <Badge variant="default">{Math.round(t.team_health_score * 100)}% Health</Badge>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 my-4 p-3 bg-slate-950/60 rounded-xl border border-slate-800/80 text-xs">
                  <div>
                    <span className="text-slate-500 block">Team Lead</span>
                    <strong className="text-indigo-400">{t.team_lead_id}</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Members</span>
                    <strong className="text-white">{t.member_ids.length} Agents</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Budget</span>
                    <strong className="text-emerald-400">${t.max_budget_usd}</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Target SLA</span>
                    <strong className="text-amber-400">{t.sla_hours}h</strong>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1.5">
                  {t.required_skills.map((s, idx) => (
                    <span key={idx} className="text-[10px] px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-slate-300">
                      {s}
                    </span>
                  ))}
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
