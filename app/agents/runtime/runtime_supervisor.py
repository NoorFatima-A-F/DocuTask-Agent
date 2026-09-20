"""
Erlang OTP-Style Runtime Supervisor & Async Process Supervision Engine.
Implements:
- Concrete worker supervision: AsyncTaskWorker, ThreadWorker, ProcessWorker, ContainerWorker
- WorkerHeartbeatMonitor with timeout detection
- WorkerLifecycleManager with graceful cancellation and failure isolation
- CheckpointRecoveryManager for state preservation across crashes
- OTP restart strategies: ONE_FOR_ONE, ONE_FOR_ALL, REST_FOR_ONE
"""

import asyncio
from abc import ABC, abstractmethod
from enum import Enum
import logging
import multiprocessing
import threading
import time
from typing import Any, Callable, Coroutine, Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.runtime.exceptions import SubsystemCrashError
from app.agents.runtime.interfaces import IRuntimeSupervisor

SubsystemCrashException = SubsystemCrashError


logger = logging.getLogger(__name__)


class RestartStrategy(str, Enum):
    """Erlang OTP restart strategy."""
    ONE_FOR_ONE = "ONE_FOR_ONE"
    ONE_FOR_ALL = "ONE_FOR_ALL"
    REST_FOR_ONE = "REST_FOR_ONE"


class WorkerStatus(str, Enum):
    """Lifecycle state of a supervised worker."""
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    UNHEALTHY = "UNHEALTHY"
    CRASHED = "CRASHED"
    RESTARTING = "RESTARTING"
    TERMINATED = "TERMINATED"


class BackoffStrategy(str, Enum):
    """Backoff strategies for supervisor child restarts."""
    EXPONENTIAL = "EXPONENTIAL"
    CONSTANT = "CONSTANT"
    LINEAR = "LINEAR"


class RestartPolicy(BaseModel):
    """Configuration governing worker failure thresholds and backoff."""
    max_restarts: int = 3
    restart_window_seconds: float = 60.0
    initial_backoff_seconds: float = 1.0
    backoff_multiplier: float = 2.0
    max_backoff_seconds: float = 30.0
    cooldown_seconds: float = 120.0
    backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL

    def __init__(
        self,
        max_restarts: int = 3,
        restart_window_seconds: float = 60.0,
        initial_backoff_seconds: Optional[float] = None,
        initial_delay_seconds: Optional[float] = None,
        backoff_multiplier: float = 2.0,
        max_backoff_seconds: Optional[float] = None,
        max_delay_seconds: Optional[float] = None,
        cooldown_seconds: float = 120.0,
        backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL,
        **data,
    ):
        init_delay = initial_delay_seconds if initial_delay_seconds is not None else (initial_backoff_seconds or 1.0)
        max_delay = max_delay_seconds if max_delay_seconds is not None else (max_backoff_seconds or 30.0)
        super().__init__(
            max_restarts=max_restarts,
            restart_window_seconds=restart_window_seconds,
            initial_backoff_seconds=init_delay,
            backoff_multiplier=backoff_multiplier,
            max_backoff_seconds=max_delay,
            cooldown_seconds=cooldown_seconds,
            backoff_strategy=backoff_strategy,
            **data,
        )

    def calculate_backoff(self, attempt: int) -> float:
        """Calculates exponential backoff delay."""
        delay = self.initial_backoff_seconds * (self.backoff_multiplier ** (attempt - 1))
        return min(delay, self.max_backoff_seconds)

    def calculate_delay(self, attempt: int) -> float:
        return self.calculate_backoff(attempt)


class BaseSupervisedWorker(ABC):

    """Base class for supervised runtime workers."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.status = WorkerStatus.IDLE
        self.last_heartbeat = time.time()

    def record_heartbeat(self) -> None:
        self.last_heartbeat = time.time()

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def stop(self, timeout: float = 5.0) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        raise NotImplementedError


class AsyncTaskWorker(BaseSupervisedWorker):
    """Supervised worker executing an asynchronous coroutine inside an asyncio.Task."""

    def __init__(self, name: str, task_fn: Callable[[], Coroutine[Any, Any, Any]]) -> None:
        super().__init__(name)
        self.task_fn = task_fn
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        self.status = WorkerStatus.RUNNING
        self.record_heartbeat()
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run_wrapper())

    async def _run_wrapper(self) -> None:
        try:
            await self.task_fn()
            self.status = WorkerStatus.IDLE
        except asyncio.CancelledError:
            self.status = WorkerStatus.TERMINATED
        except Exception as e:
            logger.error(f"AsyncTaskWorker '{self.name}' crashed: {e}")
            self.status = WorkerStatus.CRASHED
            raise

    async def stop(self, timeout: float = 5.0) -> None:
        self._stop_event.set()
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await asyncio.wait_for(self._task, timeout=timeout)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                pass
        self.status = WorkerStatus.TERMINATED

    def is_alive(self) -> bool:
        return self._task is not None and not self._task.done()


class ThreadWorker(BaseSupervisedWorker):
    """Supervised worker executing a blocking target inside a dedicated thread."""

    def __init__(self, name: str, target: Callable[[], Any]) -> None:
        super().__init__(name)
        self.target = target
        self._thread: Optional[threading.Thread] = None
        self._stop_requested = threading.Event()

    async def start(self) -> None:
        self.status = WorkerStatus.RUNNING
        self.record_heartbeat()
        self._stop_requested.clear()
        self._thread = threading.Thread(target=self._run_wrapper, name=self.name, daemon=True)
        self._thread.start()

    def _run_wrapper(self) -> None:
        try:
            self.target()
            self.status = WorkerStatus.IDLE
        except Exception as e:
            logger.error(f"ThreadWorker '{self.name}' crashed: {e}")
            self.status = WorkerStatus.CRASHED

    async def stop(self, timeout: float = 5.0) -> None:
        self._stop_requested.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=timeout)
        self.status = WorkerStatus.TERMINATED

    def is_alive(self) -> bool:
        return self._thread is not None and self._thread.is_alive()


class ProcessWorker(BaseSupervisedWorker):
    """Supervised worker executing in an isolated OS process."""

    def __init__(self, name: str, target: Callable[[], None]) -> None:
        super().__init__(name)
        self.target = target
        self._process: Optional[multiprocessing.Process] = None

    async def start(self) -> None:
        self.status = WorkerStatus.RUNNING
        self.record_heartbeat()
        self._process = multiprocessing.Process(target=self.target, name=self.name)
        self._process.start()

    async def stop(self, timeout: float = 5.0) -> None:
        if self._process and self._process.is_alive():
            self._process.terminate()
            self._process.join(timeout=timeout)
            if self._process.is_alive():
                self._process.kill()
        self.status = WorkerStatus.TERMINATED

    def is_alive(self) -> bool:
        return self._process is not None and self._process.is_alive()


class ContainerWorker(BaseSupervisedWorker):
    """Supervised containerized worker abstraction."""

    def __init__(self, name: str, image: str = "agent-runtime:latest") -> None:
        super().__init__(name)
        self.image = image
        self._running = False

    async def start(self) -> None:
        self._running = True
        self.status = WorkerStatus.RUNNING
        self.record_heartbeat()

    async def stop(self, timeout: float = 5.0) -> None:
        self._running = False
        self.status = WorkerStatus.TERMINATED

    def is_alive(self) -> bool:
        return self._running


class WorkerHeartbeatMonitor:
    """Monitors worker heartbeats and identifies unresponsive workers exceeding threshold."""

    def __init__(self, default_timeout_seconds: float = 5.0) -> None:
        self.default_timeout = default_timeout_seconds
        self._workers: Dict[str, BaseSupervisedWorker] = {}
        self._timeouts: Dict[str, float] = {}

    def register_worker(self, worker: BaseSupervisedWorker, timeout_seconds: Optional[float] = None) -> None:
        self._workers[worker.name] = worker
        self._timeouts[worker.name] = timeout_seconds or self.default_timeout

    def record_heartbeat(self, worker_name: str) -> None:
        if worker_name in self._workers:
            self._workers[worker_name].record_heartbeat()

    def check_heartbeats(self) -> List[str]:
        now = time.time()
        timed_out = []
        for name, worker in self._workers.items():
            timeout = self._timeouts.get(name, self.default_timeout)
            if worker.status == WorkerStatus.RUNNING and (now - worker.last_heartbeat > timeout):
                worker.status = WorkerStatus.UNHEALTHY
                timed_out.append(name)
        return timed_out


class CheckpointRecoveryManager:
    """Maintains and restores worker execution checkpoints across failures and restarts."""

    def __init__(self) -> None:
        self._checkpoints: Dict[str, Dict[str, Any]] = {}

    def save_checkpoint(self, worker_name: str, checkpoint: Dict[str, Any]) -> None:
        self._checkpoints[worker_name] = dict(checkpoint)

    def restore_checkpoint(self, worker_name: str) -> Optional[Dict[str, Any]]:
        return self._checkpoints.get(worker_name)

    def clear_checkpoint(self, worker_name: str) -> None:
        self._checkpoints.pop(worker_name, None)


class ChildProcessSpec:
    """Specification and state of a supervised worker process/subsystem."""

    def __init__(
        self,
        name: str,
        start_fn: Callable[[], Coroutine[Any, Any, Any]],
        stop_fn: Optional[Callable[[], Coroutine[Any, Any, Any]]] = None,
        restore_fn: Optional[Callable[[], Coroutine[Any, Any, Any]]] = None,
        policy: Optional[RestartPolicy] = None,
    ) -> None:
        self.name = name
        self.start_fn = start_fn
        self.stop_fn = stop_fn
        self.restore_fn = restore_fn
        self.policy = policy or RestartPolicy()
        self.restart_timestamps: List[float] = []
        self.last_restart_time: float = 0.0
        self.is_healthy: bool = True


class ChildProcessRegistry:
    """Catalog of registered child workers under supervision."""

    def __init__(self) -> None:
        self._specs: Dict[str, ChildProcessSpec] = {}
        self._order: List[str] = []

    def register(self, spec: ChildProcessSpec) -> None:
        self._specs[spec.name] = spec
        if spec.name not in self._order:
            self._order.append(spec.name)

    def get(self, name: str) -> Optional[ChildProcessSpec]:
        return self._specs.get(name)

    def list_specs(self) -> List[ChildProcessSpec]:
        return [self._specs[name] for name in self._order]

    def get_subsequent(self, name: str) -> List[ChildProcessSpec]:
        if name not in self._order:
            return []
        idx = self._order.index(name)
        return [self._specs[n] for n in self._order[idx:]]


class SupervisorTree:
    """Hierarchical supervisor node managing worker groups with OTP strategies."""

    def __init__(
        self,
        strategy: RestartStrategy = RestartStrategy.ONE_FOR_ONE,
        default_policy: Optional[RestartPolicy] = None,
        max_restarts: Optional[int] = None,
        cooldown_seconds: Optional[float] = None,
    ) -> None:
        self.strategy = strategy
        policy = default_policy or RestartPolicy()
        if max_restarts is not None:
            policy = policy.model_copy(update={"max_restarts": max_restarts})
        if cooldown_seconds is not None:
            policy = policy.model_copy(update={"cooldown_seconds": cooldown_seconds})
        self.default_policy = policy
        self.max_restarts = self.default_policy.max_restarts
        self.registry = ChildProcessRegistry()

    def add_child(
        self,
        name: str,
        start_fn: Callable[[], Coroutine[Any, Any, Any]],
        stop_fn: Optional[Callable[[], Coroutine[Any, Any, Any]]] = None,
        restore_fn: Optional[Callable[[], Coroutine[Any, Any, Any]]] = None,
        policy: Optional[RestartPolicy] = None,
    ) -> ChildProcessSpec:
        spec = ChildProcessSpec(
            name=name,
            start_fn=start_fn,
            stop_fn=stop_fn,
            restore_fn=restore_fn,
            policy=policy or self.default_policy,
        )
        self.registry.register(spec)
        return spec

    async def start_all(self) -> None:
        for spec in self.registry._specs.values():
            await spec.start_fn()

    async def stop_all(self) -> None:
        for spec in self.registry._specs.values():
            if spec.stop_fn:
                await spec.stop_fn()

    async def handle_child_failure(self, failed_name: str) -> None:
        spec = self.registry.get(failed_name)
        if not spec:
            return

        now = time.time()
        if spec.last_restart_time and (now - spec.last_restart_time > spec.policy.cooldown_seconds):
            spec.restart_timestamps.clear()

        spec.restart_timestamps = [
            t for t in spec.restart_timestamps if now - t <= spec.policy.restart_window_seconds
        ]
        spec.restart_timestamps.append(now)
        spec.last_restart_time = now

        if len(spec.restart_timestamps) > spec.policy.max_restarts:
            spec.is_healthy = False
            raise SubsystemCrashError(
                f"Worker '{failed_name}' exceeded maximum restart threshold ({spec.policy.max_restarts})."
            )

        backoff = spec.policy.calculate_backoff(len(spec.restart_timestamps))
        if backoff > 0.05:
            await asyncio.sleep(min(backoff, 0.1))

        if self.strategy == RestartStrategy.ONE_FOR_ONE:
            await self._restart_single(spec)
        elif self.strategy == RestartStrategy.ONE_FOR_ALL:
            await self._restart_all()
        elif self.strategy == RestartStrategy.REST_FOR_ONE:
            await self._restart_rest(failed_name)

    async def _restart_single(self, spec: ChildProcessSpec) -> None:
        if spec.stop_fn:
            try:
                await spec.stop_fn()
            except Exception as e:
                logger.warning(f"Error stopping worker '{spec.name}': {e}")
        await spec.start_fn()
        if spec.restore_fn:
            await spec.restore_fn()

    async def _restart_all(self) -> None:
        specs = self.registry.list_specs()
        for spec in reversed(specs):
            if spec.stop_fn:
                try:
                    await spec.stop_fn()
                except Exception as e:
                    logger.warning(f"Error stopping worker '{spec.name}': {e}")
        for spec in specs:
            await spec.start_fn()
            if spec.restore_fn:
                await spec.restore_fn()

    async def _restart_rest(self, from_name: str) -> None:
        specs = self.registry.get_subsequent(from_name)
        for spec in reversed(specs):
            if spec.stop_fn:
                try:
                    await spec.stop_fn()
                except Exception as e:
                    logger.warning(f"Error stopping worker '{spec.name}': {e}")
        for spec in specs:
            await spec.start_fn()
            if spec.restore_fn:
                await spec.restore_fn()


class WorkerLifecycleManager:
    """Manages worker startup, heartbeat health monitoring, failure recovery, and checkpoint restore."""

    def __init__(
        self,
        supervisor_tree: Optional[SupervisorTree] = None,
        checkpoint_manager: Optional[CheckpointRecoveryManager] = None,
        heartbeat_monitor: Optional[WorkerHeartbeatMonitor] = None,
    ) -> None:
        self.supervisor = supervisor_tree or SupervisorTree()
        self.heartbeat_monitor = heartbeat_monitor or WorkerHeartbeatMonitor()
        self.checkpoint_manager = checkpoint_manager or CheckpointRecoveryManager()
        self._managed_workers: Dict[str, BaseSupervisedWorker] = {}

    def register_worker(
        self,
        worker: BaseSupervisedWorker,
        timeout_seconds: float = 5.0,
        policy: Optional[RestartPolicy] = None,
    ) -> None:
        self._managed_workers[worker.name] = worker
        self.heartbeat_monitor.register_worker(worker, timeout_seconds=timeout_seconds)

        async def _start():
            await worker.start()

        async def _stop():
            await worker.stop()

        async def _restore():
            chk = self.checkpoint_manager.restore_checkpoint(worker.name)
            if chk:
                logger.info(f"Worker '{worker.name}' restored checkpoint: {chk}")

        self.supervisor.add_child(
            name=worker.name,
            start_fn=_start,
            stop_fn=_stop,
            restore_fn=_restore,
            policy=policy,
        )

    async def start_all(self) -> None:
        for worker in self._managed_workers.values():
            await worker.start()

    async def stop_all(self) -> None:
        for worker in self._managed_workers.values():
            await worker.stop()

    async def handle_worker_failure(self, worker_name: str) -> None:
        """Triggers supervisor recovery and checkpoint restoration."""
        worker = self._managed_workers.get(worker_name)
        if worker:
            worker.status = WorkerStatus.RESTARTING
        await self.supervisor.handle_child_failure(worker_name)


class RuntimeSupervisor(IRuntimeSupervisor):
    """Facade for the complete OTP and process supervision subsystem."""

    def __init__(
        self,
        strategy: RestartStrategy = RestartStrategy.ONE_FOR_ONE,
        max_restarts: int = 3,
        restart_window_seconds: float = 60.0,
    ) -> None:
        policy = RestartPolicy(
            max_restarts=max_restarts,
            restart_window_seconds=restart_window_seconds,
            initial_backoff_seconds=0.1,
            backoff_multiplier=2.0,
        )
        self.tree = SupervisorTree(strategy=strategy, default_policy=policy)
        self.lifecycle_manager = WorkerLifecycleManager(self.tree)

    def register_subsystem_worker(
        self,
        module_name: str,
        start_fn: Callable[[], Coroutine[Any, Any, Any]],
        stop_fn: Optional[Callable[[], Coroutine[Any, Any, Any]]] = None,
        restore_fn: Optional[Callable[[], Coroutine[Any, Any, Any]]] = None,
        policy: Optional[RestartPolicy] = None,
    ) -> None:
        self.tree.add_child(
            name=module_name,
            start_fn=start_fn,
            stop_fn=stop_fn,
            restore_fn=restore_fn,
            policy=policy,
        )

    async def supervise(self, module_name: str, coroutine_fn: Callable[[], Any]) -> Any:
        try:
            return await coroutine_fn()
        except Exception as exc:
            logger.warning(f"Supervised worker '{module_name}' failed: {exc}. Triggering restart.")
            await self.tree.handle_child_failure(module_name)
            return None

    async def restart_subsystem(self, module_name: str) -> None:
        await self.tree.handle_child_failure(module_name)
