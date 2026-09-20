import { jsx as _jsx } from "react/jsx-runtime";
import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { initialChatMessages, initialAgentInbox, initialHumanFeedbackItems, initialTimelineEvents, initialMemoryCausalNodes, initialConfidenceConstituents, initialReplaySnapshots, initialWorkspaceTasks, } from '../services/mockWorkspaceData';
const WorkspaceContext = createContext(null);
export const WorkspaceProvider = ({ children }) => {
    const [activeTab, setActiveTab] = useState('CONVERSATION');
    const [chatMessages, setChatMessages] = useState(initialChatMessages);
    const [agentInbox, setAgentInbox] = useState(initialAgentInbox);
    const [selectedAgentRole, setSelectedAgentRole] = useState('PLANNER');
    const [feedbackItems, setFeedbackItems] = useState(initialHumanFeedbackItems);
    const [timelineEvents, setTimelineEvents] = useState(initialTimelineEvents);
    const [memoryNodes] = useState(initialMemoryCausalNodes);
    const [selectedMemoryNodeId, setSelectedMemoryNodeId] = useState('node_failure');
    const [confidenceConstituents, setConfidenceConstituents] = useState(initialConfidenceConstituents);
    const [replaySnapshots] = useState(initialReplaySnapshots);
    const [currentReplayStep, setCurrentReplayStep] = useState(5);
    const [isReplaying, setIsReplaying] = useState(false);
    const [tasks, setTasks] = useState(initialWorkspaceTasks);
    // Demo Controller State
    const [isDemoRunning, setIsDemoRunning] = useState(false);
    const [demoProgressPhase, setDemoProgressPhase] = useState('IDLE');
    // Replay Auto-Playback Timer
    useEffect(() => {
        if (!isReplaying)
            return;
        const interval = setInterval(() => {
            setCurrentReplayStep((prev) => {
                if (prev >= replaySnapshots.length) {
                    setIsReplaying(false);
                    return prev;
                }
                return prev + 1;
            });
        }, 2500);
        return () => clearInterval(interval);
    }, [isReplaying, replaySnapshots.length]);
    // Conversational Command Engine (Transforms Natural Language -> Intent -> Plan Update -> Action)
    const sendUserCommand = useCallback((commandText) => {
        const userMsg = {
            id: `msg_user_${Date.now()}`,
            sender: 'HUMAN',
            timestampUtc: new Date().toISOString().substring(11, 19),
            text: commandText,
        };
        setChatMessages((prev) => [...prev, userMsg]);
        // Simulate AI Coworker Cognitive Deliberation & Intelligent Response
        setTimeout(() => {
            const lower = commandText.toLowerCase();
            let aiText = '';
            let actionTaken = undefined;
            let planUpdate = undefined;
            let quickActions = undefined;
            let role = 'PLANNER';
            if (lower.includes('confidence') || lower.includes('drop') || lower.includes('explain')) {
                role = 'STATISTICS';
                aiText = 'Confidence is currently 97.2% backed by n=53 verified holdout observations (margin of error ±2.3%, p=0.0012). No statistical regressions were detected.';
                quickActions = ['View confidence breakdown', 'Inspect 53 evidence patches', 'Run cross-validation'];
            }
            else if (lower.includes('retry') || lower.includes('ocr') || lower.includes('contrast')) {
                role = 'PLANNER';
                aiText = 'Received instruction. I am replanning our execution graph to execute a high-pass adaptive contrast optimization pass with Bayesian hyperparameter refinement.';
                actionTaken = 'DAG_MUTATION: REPLAN_ADAPTIVE_OCR';
                planUpdate = [
                    'Preprocess: Injected local quadrant contrast boosting',
                    'Tune: Run 10 Bayesian trials for optimal binarization x*',
                    'Validate: Sample size verification with power 0.84',
                ];
                quickActions = ['Approve plan adaptation', 'Inspect risk vectors', 'View task board'];
            }
            else if (lower.includes('benchmark') || lower.includes('report') || lower.includes('generate')) {
                role = 'COORDINATOR';
                aiText = 'Generating SLSA Level 3+ certified empirical report and LaTeX research table diff linking all claims to underlying SHA-256 evidence digests.';
                actionTaken = 'ARTIFACT_GENERATION: LATEX_RESEARCH_DIFF';
                quickActions = ['Download research report', 'Inspect Merkle signatures', 'Replay mission'];
            }
            else {
                role = 'COORDINATOR';
                aiText = `Understood: "${commandText}". I have dispatched the request to the Planner and Memory agents to update our mission constraints.`;
                quickActions = ['Improve invoice extraction', 'View live thought stream', 'Check agent inbox'];
            }
            const aiMsg = {
                id: `msg_ai_${Date.now()}`,
                sender: 'AI_COWORKER',
                agentRole: role,
                timestampUtc: new Date().toISOString().substring(11, 19),
                text: aiText,
                actionTaken,
                proposedPlanUpdate: planUpdate,
                suggestedQuickActions: quickActions,
                confidenceScore: 0.972,
            };
            setChatMessages((prev) => [...prev, aiMsg]);
            // Add to timeline events
            const newTimeline = {
                id: `tl_${Date.now()}`,
                timestampUtc: new Date().toISOString(),
                timeDisplay: new Date().toISOString().substring(11, 19),
                agentRole: role,
                agentName: `${role.charAt(0) + role.slice(1).toLowerCase()} Agent`,
                eventTitle: actionTaken ? `Action Dispatched: ${actionTaken}` : `Deliberation: ${commandText.substring(0, 30)}...`,
                eventDescription: aiText,
                stageName: 'PLAN',
                confidenceScore: 0.972,
            };
            setTimelineEvents((prev) => [newTimeline, ...prev]);
        }, 600);
    }, []);
    const selectAgentInbox = useCallback((role) => {
        setSelectedAgentRole(role);
    }, []);
    const sendAgentDirectMessage = useCallback((targetRole, messageBody) => {
        setAgentInbox((prev) => prev.map((agent) => {
            if (agent.agentRole === targetRole) {
                const newMsg = {
                    id: `msg_dm_${Date.now()}`,
                    fromRole: 'OPERATOR',
                    timestampUtc: new Date().toISOString().substring(11, 19),
                    body: messageBody,
                };
                return {
                    ...agent,
                    unreadMessagesCount: agent.unreadMessagesCount + 1,
                    recentMessages: [...agent.recentMessages, newMsg],
                };
            }
            return agent;
        }));
    }, []);
    const addFeedbackItem = useCallback((item) => {
        const newFeedback = {
            ...item,
            id: `fb_${Date.now()}`,
            submittedAtUtc: new Date().toISOString().substring(11, 19),
            status: 'PENDING_REVIEW',
        };
        setFeedbackItems((prev) => [newFeedback, ...prev]);
    }, []);
    const convertFeedbackToMemory = useCallback((feedbackId) => {
        setFeedbackItems((prev) => prev.map((fb) => fb.id === feedbackId
            ? {
                ...fb,
                status: 'CONVERTED_TO_MEMORY',
                appliedLessonSummary: `Distilled invariant: "${fb.fieldName}" correction stored in Long-Term Memory (R=0.98).`,
            }
            : fb));
        // Reinforce confidence
        setConfidenceConstituents((prev) => prev.map((c) => c.category === 'HUMAN_FEEDBACK'
            ? { ...c, contributionPercentage: c.contributionPercentage + 1, sampleSize: (c.sampleSize || 0) + 1 }
            : c));
    }, []);
    const convertFeedbackToBenchmark = useCallback((feedbackId) => {
        setFeedbackItems((prev) => prev.map((fb) => fb.id === feedbackId
            ? {
                ...fb,
                status: 'CONVERTED_TO_BENCHMARK',
                appliedLessonSummary: `Added "${fb.documentId}" as gold-standard benchmark test case.`,
            }
            : fb));
    }, []);
    const convertFeedbackToRule = useCallback((feedbackId) => {
        setFeedbackItems((prev) => prev.map((fb) => fb.id === feedbackId
            ? {
                ...fb,
                status: 'CONVERTED_TO_RULE',
                appliedLessonSummary: `Governance rule locked: Regex validator enforced on "${fb.fieldName}".`,
            }
            : fb));
    }, []);
    const selectMemoryNode = useCallback((nodeId) => {
        setSelectedMemoryNodeId(nodeId);
    }, []);
    const setReplayStep = useCallback((step) => {
        setCurrentReplayStep(Math.max(1, Math.min(step, replaySnapshots.length)));
    }, [replaySnapshots.length]);
    const playReplay = useCallback(() => setIsReplaying(true), []);
    const pauseReplay = useCallback(() => setIsReplaying(false), []);
    const stepForwardReplay = useCallback(() => {
        setCurrentReplayStep((prev) => Math.min(prev + 1, replaySnapshots.length));
    }, [replaySnapshots.length]);
    const stepBackwardReplay = useCallback(() => {
        setCurrentReplayStep((prev) => Math.max(prev - 1, 1));
    }, []);
    const updateTaskStatus = useCallback((taskId, newStatus) => {
        setTasks((prev) => prev.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t)));
    }, []);
    // Autonomous One-Click Demo Mode runner
    const startAutonomousDemo = useCallback(() => {
        setIsDemoRunning(true);
        setActiveTab('CONVERSATION');
        setDemoProgressPhase('STARTING');
        const demoSteps = [
            {
                phase: '1. Goal Understanding',
                action: () => sendUserCommand('Optimize noisy invoice extraction on degraded thermal receipts'),
                delay: 500,
            },
            {
                phase: '2. Multi-Agent Deliberation',
                action: () => setActiveTab('AGENT_INBOX'),
                delay: 3500,
            },
            {
                phase: '3. Task Execution & Bayesian Optimization',
                action: () => setActiveTab('TASK_BOARD'),
                delay: 6500,
            },
            {
                phase: '4. Human Feedback Reinforcement',
                action: () => {
                    setActiveTab('FEEDBACK_LOOP');
                    if (feedbackItems[0]) {
                        convertFeedbackToMemory(feedbackItems[0].id);
                    }
                },
                delay: 9500,
            },
            {
                phase: '5. Causal Memory Graph Inspection',
                action: () => setActiveTab('MEMORY_GRAPH'),
                delay: 13000,
            },
            {
                phase: '6. Statistical Confidence Target Satisfied (97.2%)',
                action: () => {
                    setActiveTab('CONFIDENCE_EXPLORER');
                    setDemoProgressPhase('COMPLETED');
                    setIsDemoRunning(false);
                },
                delay: 16500,
            },
        ];
        demoSteps.forEach((step) => {
            setTimeout(() => {
                setDemoProgressPhase(step.phase);
                step.action();
            }, step.delay);
        });
    }, [sendUserCommand, feedbackItems, convertFeedbackToMemory]);
    const stopAutonomousDemo = useCallback(() => {
        setIsDemoRunning(false);
        setDemoProgressPhase('IDLE');
    }, []);
    return (_jsx(WorkspaceContext.Provider, { value: {
            activeTab,
            setActiveTab,
            chatMessages,
            sendUserCommand,
            agentInbox,
            selectedAgentRole,
            selectAgentInbox,
            sendAgentDirectMessage,
            feedbackItems,
            addFeedbackItem,
            convertFeedbackToMemory,
            convertFeedbackToBenchmark,
            convertFeedbackToRule,
            timelineEvents,
            memoryNodes,
            selectedMemoryNodeId,
            selectMemoryNode,
            confidenceConstituents,
            replaySnapshots,
            currentReplayStep,
            isReplaying,
            setReplayStep,
            playReplay,
            pauseReplay,
            stepForwardReplay,
            stepBackwardReplay,
            tasks,
            updateTaskStatus,
            isDemoRunning,
            demoProgressPhase,
            startAutonomousDemo,
            stopAutonomousDemo,
        }, children: children }));
};
export const useWorkspace = () => {
    const context = useContext(WorkspaceContext);
    if (!context) {
        throw new Error('useWorkspace must be used within a WorkspaceProvider');
    }
    return context;
};
