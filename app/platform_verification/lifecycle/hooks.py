from typing import Callable, Dict, List
from app.platform_verification.lifecycle.context import VerificationExecutionContext

class LifecycleHooks:
    def __init__(self):
        self._hooks: Dict[str, List[Callable[[VerificationExecutionContext], None]]] = {}

    def register_hook(self, hook_point: str, callback: Callable[[VerificationExecutionContext], None]) -> None:
        if hook_point not in self._hooks:
            self._hooks[hook_point] = []
        self._hooks[hook_point].append(callback)

    def trigger_hook(self, hook_point: str, context: VerificationExecutionContext) -> None:
        for callback in self._hooks.get(hook_point, []):
            callback(context)

lifecycle_hooks = LifecycleHooks()
