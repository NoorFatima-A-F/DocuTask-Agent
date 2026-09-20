/**
 * Runtime Telemetry Context & Provider
 * 
 * Manages live execution events, derived metrics, agent statuses, and OpenTelemetry
 * correlation traces streamed directly from the real autonomous runtime backend.
 */

import React, { createContext, useContext, useEffect, useState, useCallback, useRef } from 'react';
import type {
  RuntimeEvent,
  MissionMetricsSummary,
  RuntimeAgentStatus,
  RuntimeMissionState,
  ReplaySnapshotState,
} from '../types/runtimeTelemetry';
import { runtimeApiClient, type HumanFeedbackPayload } from '../services/runtimeApiClient';

interface RuntimeTelemetryContextValue {
  events: RuntimeEvent[];
  metrics: MissionMetricsSummary | null;
  agents: RuntimeAgentStatus[];
  mission: RuntimeMissionState | null;
  isConnected: boolean;
  isLoading: boolean;
  error: string | null;
  selectedEventForInspector: RuntimeEvent | null;
  replaySnapshot: ReplaySnapshotState | null;
  
  // Actions
  setSelectedEventForInspector: (event: RuntimeEvent | null) => void;
  startMission: (goal: string, scenarioType?: string) => Promise<string>;
  sendCommand: (commandText: string, targetAgent?: string) => Promise<any>;
  submitFeedback: (payload: Omit<HumanFeedbackPayload, 'missionId'>) => Promise<any>;
  fetchReplayStep: (step: number) => Promise<ReplaySnapshotState>;
  refreshAll: () => Promise<void>;
}

const RuntimeTelemetryContext = createContext<RuntimeTelemetryContextValue | null>(null);

export const RuntimeTelemetryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [events, setEvents] = useState<RuntimeEvent[]>([]);
  const [metrics, setMetrics] = useState<MissionMetricsSummary | null>(null);
  const [agents, setAgents] = useState<RuntimeAgentStatus[]>([]);
  const [mission, setMission] = useState<RuntimeMissionState | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedEventForInspector, setSelectedEventForInspector] = useState<RuntimeEvent | null>(null);
  const [replaySnapshot, setReplaySnapshot] = useState<ReplaySnapshotState | null>(null);

  const activeMissionIdRef = useRef<string | undefined>(undefined);

  const refreshAll = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const [fetchedEvents, fetchedMetrics, fetchedAgents, fetchedMission] = await Promise.all([
        runtimeApiClient.fetchEvents(activeMissionIdRef.current, 300).catch(() => []),
        runtimeApiClient.fetchMetrics(activeMissionIdRef.current).catch(() => null),
        runtimeApiClient.fetchAgents().catch(() => []),
        runtimeApiClient.fetchMission(activeMissionIdRef.current).catch(() => null),
      ]);

      setEvents(fetchedEvents);
      setMetrics(fetchedMetrics);
      setAgents(fetchedAgents);
      setMission(fetchedMission);
      if (fetchedMission?.mission_id) {
        activeMissionIdRef.current = fetchedMission.mission_id;
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch runtime telemetry');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Initialize and connect SSE stream
  useEffect(() => {
    refreshAll();

    let unsubscribeStream: (() => void) | null = null;
    try {
      unsubscribeStream = runtimeApiClient.subscribeEventStream(
        (newEvent: RuntimeEvent) => {
          setIsConnected(true);
          setEvents((prev) => {
            // Deduplicate by event_id
            if (prev.some((e) => e.event_id === newEvent.event_id)) {
              return prev;
            }
            return [newEvent, ...prev].slice(0, 5000);
          });

          // If a new mission is started or state changes, trigger background metric/agent sync
          if (
            newEvent.event_type.includes('Mission') ||
            newEvent.event_type.includes('Worker') ||
            newEvent.event_type.includes('Planner') ||
            newEvent.event_type.includes('Memory')
          ) {
            runtimeApiClient.fetchMetrics(newEvent.mission_id).then(setMetrics).catch(() => {});
            runtimeApiClient.fetchAgents().then(setAgents).catch(() => {});
            runtimeApiClient.fetchMission(newEvent.mission_id).then(setMission).catch(() => {});
          }
        },
        () => {
          setIsConnected(false);
        }
      );
      setIsConnected(true);
    } catch (err) {
      setIsConnected(false);
    }

    // Polling fallback every 3 seconds for dynamic heartbeat intervals
    const pollInterval = setInterval(() => {
      runtimeApiClient.fetchAgents().then(setAgents).catch(() => {});
      runtimeApiClient.fetchMetrics(activeMissionIdRef.current).then(setMetrics).catch(() => {});
    }, 3000);

    return () => {
      if (unsubscribeStream) unsubscribeStream();
      clearInterval(pollInterval);
    };
  }, [refreshAll]);

  const startMission = useCallback(
    async (goal: string, scenarioType?: string): Promise<string> => {
      const res = await runtimeApiClient.startMission({
        goal,
        scenarioType: scenarioType || 'THERMAL_INVOICE_AUDIT',
      });
      activeMissionIdRef.current = res.mission_id;
      await refreshAll();
      return res.mission_id;
    },
    [refreshAll]
  );

  const sendCommand = useCallback(
    async (commandText: string, targetAgent?: string): Promise<any> => {
      const missionId = activeMissionIdRef.current || mission?.mission_id || 'default_mission';
      const res = await runtimeApiClient.sendCommand({
        missionId,
        commandText,
        targetAgent,
      });
      await refreshAll();
      return res;
    },
    [mission, refreshAll]
  );

  const submitFeedback = useCallback(
    async (payload: Omit<HumanFeedbackPayload, 'missionId'>): Promise<any> => {
      const missionId = activeMissionIdRef.current || mission?.mission_id || 'default_mission';
      const res = await runtimeApiClient.submitFeedback({
        ...payload,
        missionId,
      });
      await refreshAll();
      return res;
    },
    [mission, refreshAll]
  );

  const fetchReplayStep = useCallback(
    async (step: number): Promise<ReplaySnapshotState> => {
      const missionId = activeMissionIdRef.current || mission?.mission_id || 'default_mission';
      const snapshot = await runtimeApiClient.fetchReplay(missionId, step);
      setReplaySnapshot(snapshot);
      return snapshot;
    },
    [mission]
  );

  return (
    <RuntimeTelemetryContext.Provider
      value={{
        events,
        metrics,
        agents,
        mission,
        isConnected,
        isLoading,
        error,
        selectedEventForInspector,
        replaySnapshot,
        setSelectedEventForInspector,
        startMission,
        sendCommand,
        submitFeedback,
        fetchReplayStep,
        refreshAll,
      }}
    >
      {children}
    </RuntimeTelemetryContext.Provider>
  );
};

export const useRuntimeTelemetry = (): RuntimeTelemetryContextValue => {
  const ctx = useContext(RuntimeTelemetryContext);
  if (!ctx) {
    throw new Error('useRuntimeTelemetry must be used within a RuntimeTelemetryProvider');
  }
  return ctx;
};
