import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const SDKExplorerView = () => {
    const [selectedSdkClass, setSelectedSdkClass] = useState('BaseAgent');
    const sdkClasses = [
        {
            name: 'BaseAgent',
            module: 'app.sdk.agent_sdk',
            description: 'Core autonomous agent interface with lifecycle hooks (on_init, execute, on_terminate) and permission scope enforcement.',
            code: `class BaseAgent(abc.ABC):
    def __init__(self, manifest: AgentManifest, context: AgentExecutionContext):
        self.manifest = manifest
        self.context = context
        self.state = AgentLifecycleState.UNINITIALIZED

    @abc.abstractmethod
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Core autonomous execution logic."""
        pass`,
        },
        {
            name: 'BasePlanner',
            module: 'app.sdk.planner_sdk',
            description: 'Abstract planner allowing plugins to propose candidate execution plans evaluated via mathematical utility optimization.',
            code: `class BasePlanner(abc.ABC):
    @abc.abstractmethod
    def generate_candidates(self, goal: str, constraints: dict, capabilities: list) -> List[CandidatePlan]:
        pass

    @abc.abstractmethod
    def select_optimal_plan(self, candidates: List[CandidatePlan], weights: dict) -> CandidatePlan:
        pass`,
        },
        {
            name: 'BaseWorker',
            module: 'app.sdk.worker_sdk',
            description: 'Specialized capability worker executing bounded tasks with millisecond SLA timers and energy telemetry.',
            code: `class BaseWorker(abc.ABC):
    @abc.abstractmethod
    def process_task(self, task: WorkerTask) -> WorkerResult:
        pass

    def probe_health(self) -> dict:
        return {"worker_id": self.worker_id, "healthy": True}`,
        },
        {
            name: 'BaseTool',
            module: 'app.sdk.tool_sdk',
            description: 'Declarative tool integration wrapper exposing JSON parameters, return schemas, cost models, and permission scopes.',
            code: `class BaseTool(abc.ABC):
    def __init__(self, schema: ToolSchema):
        self.schema = schema

    @abc.abstractmethod
    def invoke(self, arguments: dict, context: dict) -> dict:
        pass`,
        },
        {
            name: 'BasePolicyRule',
            module: 'app.sdk.policy_sdk',
            description: 'Declarative compliance and safety guardrail evaluated before any tool invocation or model call.',
            code: `class BasePolicyRule(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, action: dict, context: dict) -> bool:
        """Returns True if compliant, False otherwise."""
        pass`,
        },
    ];
    const active = sdkClasses.find((c) => c.name === selectedSdkClass) || sdkClasses[0];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Enterprise Agent SDK Explorer" }), _jsx(Badge, { variant: "success", size: "sm", children: "v2026.1 Strict Protocols" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Standardized interfaces, base classes, lifecycle hooks, and telemetry contracts ensuring zero direct coupling to runtime internals." })] }), _jsx(Badge, { variant: "outline", size: "md", children: "Python SDK 3.8+ / TypeScript Typed" })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: ["SDK Core Classes (", sdkClasses.length, ")"] }), sdkClasses.map((item) => (_jsxs(Card, { className: `p-4 cursor-pointer transition-all ${selectedSdkClass === item.name
                                    ? 'border-primary ring-1 ring-primary/40 bg-primary/5'
                                    : 'hover:border-border/80'}`, onClick: () => setSelectedSdkClass(item.name), children: [_jsx("div", { className: "font-mono text-sm font-bold text-foreground", children: item.name }), _jsx("div", { className: "font-mono text-[11px] text-muted-foreground mt-0.5", children: item.module })] }, item.name)))] }), _jsx("div", { className: "lg:col-span-2 space-y-4", children: _jsxs(Card, { className: "p-6 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-border/40 pb-3", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-lg font-bold font-mono", children: active.name }), _jsx("div", { className: "text-xs text-muted-foreground font-mono mt-0.5", children: active.module })] }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Abstract Base Class" })] }), _jsx("p", { className: "text-xs text-muted-foreground leading-relaxed", children: active.description }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "Interface Definition" }), _jsx("pre", { className: "p-4 bg-black/80 rounded-lg border border-border/40 font-mono text-xs text-emerald-400 overflow-x-auto leading-relaxed", children: active.code })] })] }) })] })] }));
};
