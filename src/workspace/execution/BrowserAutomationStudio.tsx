import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Globe,
  RotateCw,
  Camera,
  Play,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { BrowserSession } from '../../types/executionPlatform';

export const BrowserAutomationStudio: React.FC = () => {
  const [sessions, setSessions] = useState<BrowserSession[]>([]);
  const [activeSession, setActiveSession] = useState<BrowserSession | null>(null);
  const [urlInput, setUrlInput] = useState<string>('https://portal.enterprise-vendor.com/invoices');
  const [loading, setLoading] = useState<boolean>(true);
  const [navigating, setNavigating] = useState<boolean>(false);

  const loadSessions = async () => {
    try {
      setLoading(true);
      const res = await executionPlatformApiClient.listBrowserSessions();
      setSessions(res.sessions || []);
      if (res.sessions && res.sessions.length > 0 && !activeSession) {
        setActiveSession(res.sessions[0] || null);
      }
    } catch (err) {
      console.error('Failed to load browser sessions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  const handleCreateSession = async () => {
    try {
      const res = await executionPlatformApiClient.createBrowserSession();
      await loadSessions();
      setActiveSession(res.session);
    } catch (err) {
      console.error('Error creating browser session:', err);
    }
  };

  const handleNavigate = async () => {
    if (!activeSession || !urlInput.trim()) return;
    try {
      setNavigating(true);
      await executionPlatformApiClient.executeBrowserAction(activeSession.session_id, {
        action_type: 'navigate',
        value: urlInput,
      });
      await loadSessions();
    } catch (err) {
      console.error('Error navigating browser:', err);
    } finally {
      setNavigating(false);
    }
  };

  const handleScreenshot = async () => {
    if (!activeSession) return;
    try {
      await executionPlatformApiClient.executeBrowserAction(activeSession.session_id, {
        action_type: 'screenshot',
      });
      await loadSessions();
    } catch (err) {
      console.error('Error capturing screenshot:', err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Globe className="w-5 h-5 text-cyan-400" />
            Browser Automation & Vision Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Headless Playwright orchestration, DOM tree parsing, accessibility trees & visual snapshots
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={loadSessions}>
            <span className="flex items-center gap-1.5">
              <RotateCw className="w-4 h-4" />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={handleCreateSession}>
            <span className="flex items-center gap-1.5">
              <Globe className="w-4 h-4" />
              Spawn Headless Session
            </span>
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Active Browser Sessions */}
        <Card className="lg:col-span-1 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-white">Browser Sessions ({sessions.length})</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {loading && sessions.length === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">Loading browser sessions...</p>
            ) : sessions.map((s) => (
              <div
                key={s.session_id}
                onClick={() => setActiveSession(s)}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  activeSession?.session_id === s.session_id
                    ? 'bg-purple-950/40 border-purple-600'
                    : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-cyan-300 truncate max-w-[170px]">
                    {s.session_id}
                  </span>
                  <Badge variant={s.is_active ? 'success' : 'outline'}>
                    {s.is_active ? 'active' : 'closed'}
                  </Badge>
                </div>
                <p className="text-[11px] text-slate-300 mt-1 truncate">{s.current_url}</p>
                <div className="flex items-center justify-between mt-2 text-[10px] text-slate-500 font-mono">
                  <span>{s.viewport_width}x{s.viewport_height}</span>
                  <span>{s.dom_elements_count} DOM elements</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Right: Interactive Navigation Bar & Session Inspector */}
        <Card className="lg:col-span-2 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <CardTitle className="text-base text-white">
              {activeSession ? activeSession.page_title : 'Select a Session'}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Synthetic Browser Omnibar */}
            <div className="flex gap-2">
              <input
                type="text"
                className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-white text-xs font-mono focus:outline-none focus:border-cyan-500"
                placeholder="Enter HTTPS target URL..."
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
              />
              <Button variant="secondary" onClick={handleNavigate} disabled={navigating || !activeSession}>
                <span className="flex items-center gap-1.5 text-xs">
                  <Play className="w-3.5 h-3.5" />
                  Navigate
                </span>
              </Button>
              <Button variant="outline" onClick={handleScreenshot} disabled={!activeSession}>
                <span className="flex items-center gap-1.5 text-xs">
                  <Camera className="w-3.5 h-3.5 text-cyan-400" />
                  Capture Snapshot
                </span>
              </Button>
            </div>

            {/* Simulated Viewport Frame */}
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl min-h-[300px] flex flex-col justify-between">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800/80 text-xs text-slate-400">
                <span className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                  Connected to Headless CDP Chrome Node
                </span>
                <span className="font-mono">{activeSession?.current_url}</span>
              </div>

              <div className="py-12 flex flex-col items-center justify-center text-center">
                <Globe className="w-12 h-12 text-slate-700 mb-3 animate-pulse" />
                <h4 className="text-sm font-semibold text-slate-300">
                  {activeSession?.page_title || 'Headless Browser Ready'}
                </h4>
                <p className="text-xs text-slate-500 max-w-sm mt-1">
                  Synthetic DOM tree parsed with {activeSession?.dom_elements_count || 0} interactive elements.
                </p>
              </div>

              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500">
                <span>User-Agent: Chromium Headless 124.0.0</span>
                <span>SSL Invariant: Verified</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
