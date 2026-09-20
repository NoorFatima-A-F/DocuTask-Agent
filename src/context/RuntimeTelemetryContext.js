import { jsx as _jsx } from "react/jsx-runtime";
/**
 * Runtime Telemetry Context & Provider
 *
 * Manages live execution events, derived metrics, agent statuses, and OpenTelemetry
 * correlation traces streamed directly from the real autonomous runtime backend.
 */
import { createContext, useContext, useEffect, useState, useCallback, useRef } from 'react';
import { runtimeApiClient } from '../services/runtimeApiClient';
const RuntimeTelemetryContext = createContext(null);
export const RuntimeTelemetryProvider = ({ children }) => {
    const [events, setEvents] = useState([]);
    const [metrics, setMetrics] = useState(null);
    const [agents, setAgents] = useState([]);
    const [mission, setMission] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedEventForInspector, setSelectedEventForInspector] = useState(null);
    const [replaySnapshot, setReplaySnapshot] = useState(null);
    const activeMissionIdRef = useRef(undefined);
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
        }
        catch (err) {
            setError(err?.message || 'Failed to fetch runtime telemetry');
        }
        finally {
            setIsLoading(false);
        }
    }, []);
    // Initialize and connect SSE stream
    useEffect(() => {
        refreshAll();
        let unsubscribeStream = null;
        try {
            unsubscribeStream = runtimeApiClient.subscribeEventStream((newEvent) => {
                setIsConnected(true);
                setEvents((prev) => {
                    // Deduplicate by event_id
                    if (prev.some((e) => e.event_id === newEvent.event_id)) {
                        return prev;
                    }
                    return [newEvent, ...prev].slice(0, 5000);
                });
                // If a new mission is started or state changes, trigger background metric/agent sync
                if (newEvent.event_type.includes('Mission') ||
                    newEvent.event_type.includes('Worker') ||
                    newEvent.event_type.includes('Planner') ||
                    newEvent.event_type.includes('Memory')) {
                    runtimeApiClient.fetchMetrics(newEvent.mission_id).then(setMetrics).catch(() => { });
                    runtimeApiClient.fetchAgents().then(setAgents).catch(() => { });
                    runtimeApiClient.fetchMission(newEvent.mission_id).then(setMission).catch(() => { });
                }
            }, () => {
                setIsConnected(false);
            });
            setIsConnected(true);
        }
        catch (err) {
            setIsConnected(false);
        }
        // Polling fallback every 3 seconds for dynamic heartbeat intervals
        const pollInterval = setInterval(() => {
            runtimeApiClient.fetchAgents().then(setAgents).catch(() => { });
            runtimeApiClient.fetchMetrics(activeMissionIdRef.current).then(setMetrics).catch(() => { });
        }, 3000);
        return () => {
            if (unsubscribeStream)
                unsubscribeStream();
            clearInterval(pollInterval);
        };
    }, [refreshAll]);
    const startMission = useCallback(async (goal, scenarioType) => {
        const res = await runtimeApiClient.startMission({
            goal,
            scenarioType: scenarioType || 'THERMAL_INVOICE_AUDIT',
        });
        activeMissionIdRef.current = res.mission_id;
        await refreshAll();
        return res.mission_id;
    }, [refreshAll]);
    const sendCommand = useCallback(async (commandText, targetAgent) => {
        const missionId = activeMissionIdRef.current || mission?.mission_id || 'default_mission';
        const res = await runtimeApiClient.sendCommand({
            missionId,
            commandText,
            targetAgent,
        });
        await refreshAll();
        return res;
    }, [mission, refreshAll]);
    const submitFeedback = useCallback(async (payload) => {
        const missionId = activeMissionIdRef.current || mission?.mission_id || 'default_mission';
        const res = await runtimeApiClient.submitFeedback({
            ...payload,
            missionId,
        });
        await refreshAll();
        return res;
    }, [mission, refreshAll]);
    const fetchReplayStep = useCallback(async (step) => {
        const missionId = activeMissionIdRef.current || mission?.mission_id || 'default_mission';
        const snapshot = await runtimeApiClient.fetchReplay(missionId, step);
        setReplaySnapshot(snapshot);
        return snapshot;
    }, [mission]);
    return (_jsx(RuntimeTelemetryContext.Provider, { value: {
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
        }, children: children }));
};
export const useRuntimeTelemetry = () => {
    const ctx = useContext(RuntimeTelemetryContext);
    if (!ctx) {
        throw new Error('useRuntimeTelemetry must be used within a RuntimeTelemetryProvider');
    }
    return ctx;
};
