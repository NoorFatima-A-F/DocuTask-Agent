import { jsx as _jsx } from "react/jsx-runtime";
import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { initialMissionControlState } from '../services/mockMissionData';
const MissionControlContext = createContext(null);
export const MissionControlProvider = ({ children }) => {
    const [state, setState] = useState(initialMissionControlState);
    // Periodic clock and simulated thought stream ticker
    useEffect(() => {
        if (!state.isSimulatingLive || state.isPaused)
            return;
        const timer = setInterval(() => {
            setState((prev) => {
                const newElapsed = prev.mission.elapsedSeconds + 1;
                // Random thought generator every ~8 seconds
                let newThoughts = prev.thoughtStream;
                if (newElapsed % 8 === 0) {
                    const agents = [
                        'STATISTICS',
                        'REFLECTION',
                        'EVIDENCE',
                        'MEMORY',
                        'COORDINATOR',
                    ];
                    const randomAgent = agents[Math.floor(Math.random() * agents.length)];
                    const thoughts = {
                        STATISTICS: [
                            'Statistical power re-verified at 0.842 with effect size delta = +0.031.',
                            'Sample size threshold invariant satisfied: n=53 >= 48.',
                        ],
                        REFLECTION: [
                            'Holdout cross-validation loss is stable at 0.0204 across 10 folds.',
                            'Empirical F1 bounds confirmed between [0.949, 0.995].',
                        ],
                        EVIDENCE: [
                            'SHA-256 digital signature verified for batch artifact #48.',
                            'No distribution drift detected in incoming invoice resolutions.',
                        ],
                        MEMORY: [
                            'Reinforced long-term retention weight for thermal scan binarization (R=0.95).',
                            'Pareto frontier updated: (F1: 0.9796, Latency: 140ms).',
                        ],
                        COORDINATOR: [
                            'Cognition loop progress: reflection stage healthy. Approaching critique phase.',
                            'Inter-agent deliberation channel idle; no conflicting constraints.',
                        ],
                    };
                    const options = thoughts[randomAgent] || ['Agent deliberating on empirical bounds...'];
                    const randomText = options[Math.floor(Math.random() * options.length)];
                    const newMsg = {
                        id: `msg_${Date.now()}`,
                        agentRole: randomAgent,
                        agentName: `${randomAgent.charAt(0) + randomAgent.slice(1).toLowerCase()} Agent`,
                        timestampUtc: new Date().toISOString().substring(11, 19),
                        thoughtType: 'DELIBERATION',
                        content: randomText,
                        confidence: 0.975,
                    };
                    newThoughts = [newMsg, ...prev.thoughtStream.slice(0, 19)];
                }
                return {
                    ...prev,
                    mission: {
                        ...prev.mission,
                        elapsedSeconds: newElapsed,
                    },
                    thoughtStream: newThoughts,
                };
            });
        }, 1000);
        return () => clearInterval(timer);
    }, [state.isSimulatingLive, state.isPaused]);
    const pauseMission = useCallback((reason = 'User requested pause') => {
        setState((prev) => {
            const audit = {
                id: `audit_${Date.now()}`,
                timestampUtc: new Date().toISOString().substring(11, 19),
                action: 'PAUSE',
                triggeredBy: 'Operator',
                reason,
                resultingMissionState: 'PAUSED',
                auditSha256Receipt: '7a9b...auditReceipt',
            };
            return {
                ...prev,
                isPaused: true,
                mission: { ...prev.mission, currentState: 'PAUSED' },
                humanAuditLogs: [audit, ...prev.humanAuditLogs],
            };
        });
    }, []);
    const resumeMission = useCallback((reason = 'User resumed mission') => {
        setState((prev) => {
            const audit = {
                id: `audit_${Date.now()}`,
                timestampUtc: new Date().toISOString().substring(11, 19),
                action: 'RESUME',
                triggeredBy: 'Operator',
                reason,
                resultingMissionState: 'ACTIVE',
                auditSha256Receipt: '9c8d...auditReceipt',
            };
            return {
                ...prev,
                isPaused: false,
                mission: { ...prev.mission, currentState: 'ACTIVE' },
                humanAuditLogs: [audit, ...prev.humanAuditLogs],
            };
        });
    }, []);
    const approveDecision = useCallback((decisionId) => {
        setState((prev) => {
            const audit = {
                id: `audit_${Date.now()}`,
                timestampUtc: new Date().toISOString().substring(11, 19),
                action: 'APPROVE',
                triggeredBy: 'Operator',
                reason: `Approved decision ${decisionId}`,
                resultingMissionState: prev.mission.currentState,
                auditSha256Receipt: '4f2e...auditReceipt',
            };
            return {
                ...prev,
                humanAuditLogs: [audit, ...prev.humanAuditLogs],
            };
        });
    }, []);
    const rejectDecision = useCallback((decisionId, reason) => {
        setState((prev) => {
            const audit = {
                id: `audit_${Date.now()}`,
                timestampUtc: new Date().toISOString().substring(11, 19),
                action: 'REJECT',
                triggeredBy: 'Operator',
                reason: `Rejected decision ${decisionId}: ${reason}`,
                resultingMissionState: prev.mission.currentState,
                auditSha256Receipt: '5a1b...auditReceipt',
            };
            return {
                ...prev,
                humanAuditLogs: [audit, ...prev.humanAuditLogs],
            };
        });
    }, []);
    const overrideDecision = useCallback((decisionId, newAction, reason) => {
        setState((prev) => {
            const updatedDecisions = prev.decisions.map((d) => {
                if (d.id === decisionId) {
                    return {
                        ...d,
                        isHumanOverridden: true,
                        humanOverrideAction: newAction,
                        selectedAction: newAction,
                    };
                }
                return d;
            });
            const audit = {
                id: `audit_${Date.now()}`,
                timestampUtc: new Date().toISOString().substring(11, 19),
                action: 'OVERRIDE',
                triggeredBy: 'Operator',
                reason: `Overrode decision ${decisionId} to ${newAction}: ${reason}`,
                resultingMissionState: prev.mission.currentState,
                auditSha256Receipt: '3e8a...auditReceipt',
            };
            return {
                ...prev,
                decisions: updatedDecisions,
                humanAuditLogs: [audit, ...prev.humanAuditLogs],
            };
        });
    }, []);
    const abortMission = useCallback((reason) => {
        setState((prev) => {
            const audit = {
                id: `audit_${Date.now()}`,
                timestampUtc: new Date().toISOString().substring(11, 19),
                action: 'ABORT',
                triggeredBy: 'Operator',
                reason,
                resultingMissionState: 'ABORTED',
                auditSha256Receipt: '0f0f...auditReceipt',
            };
            return {
                ...prev,
                isPaused: true,
                mission: { ...prev.mission, currentState: 'ABORTED' },
                humanAuditLogs: [audit, ...prev.humanAuditLogs],
            };
        });
    }, []);
    const requestExplanation = useCallback((decisionId) => {
        setState((prev) => {
            const audit = {
                id: `audit_${Date.now()}`,
                timestampUtc: new Date().toISOString().substring(11, 19),
                action: 'REQUEST_EXPLANATION',
                triggeredBy: 'Operator',
                reason: `Requested deep statistical explanation for decision ${decisionId}`,
                resultingMissionState: prev.mission.currentState,
                auditSha256Receipt: '9a9a...auditReceipt',
            };
            return {
                ...prev,
                selectedDecisionId: decisionId,
                humanAuditLogs: [audit, ...prev.humanAuditLogs],
            };
        });
    }, []);
    const selectDagNode = useCallback((nodeId) => {
        setState((prev) => ({ ...prev, selectedDagNodeId: nodeId }));
    }, []);
    const selectDecision = useCallback((decisionId) => {
        setState((prev) => ({ ...prev, selectedDecisionId: decisionId }));
    }, []);
    const toggleLiveSimulation = useCallback(() => {
        setState((prev) => ({ ...prev, isSimulatingLive: !prev.isSimulatingLive }));
    }, []);
    const injectSentinelState = useCallback(() => {
        setState((prev) => ({
            ...prev,
            confidenceData: {
                ...prev.confidenceData,
                currentConfidence: 0,
                missingEvidenceCount: 5,
                whyConfidenceChanged: 'DATASET_UNAVAILABLE sentinel triggered. Ground truth validation partition offline.',
            },
            decisions: prev.decisions.map((d, i) => i === 0
                ? {
                    ...d,
                    sentinelState: 'INSUFFICIENT_EVIDENCE',
                    confidenceScore: 0,
                }
                : d),
        }));
    }, []);
    const resetInitialState = useCallback(() => {
        setState(initialMissionControlState);
    }, []);
    return (_jsx(MissionControlContext.Provider, { value: {
            state,
            pauseMission,
            resumeMission,
            approveDecision,
            rejectDecision,
            overrideDecision,
            abortMission,
            requestExplanation,
            selectDagNode,
            selectDecision,
            toggleLiveSimulation,
            injectSentinelState,
            resetInitialState,
        }, children: children }));
};
export const useMissionControl = () => {
    const context = useContext(MissionControlContext);
    if (!context) {
        throw new Error('useMissionControl must be used within a MissionControlProvider');
    }
    return context;
};
