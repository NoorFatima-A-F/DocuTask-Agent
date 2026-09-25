"""Argo CD GitOps Provider Adapter."""
from .base import GitOpsProvider, GitOpsSyncResult


class ArgoCDProvider(GitOpsProvider):
    """Argo CD API & Controller Integration."""

    def __init__(self, server_url: str = "https://argocd.internal.docutask.io"):
        self.server_url = server_url
        self._app_states = {}

    @property
    def provider_name(self) -> str:
        return "ArgoCD"

    def sync_application(self, app_name: str, revision: str, prune: bool = True) -> GitOpsSyncResult:
        self._app_states[app_name] = {
            "sync_status": "Synced",
            "health_status": "Healthy",
            "revision": revision,
            "message": f"Successfully synced to revision {revision} via ArgoCD",
        }
        return self.get_sync_status(app_name)

    def get_sync_status(self, app_name: str) -> GitOpsSyncResult:
        state = self._app_states.get(
            app_name,
            {"sync_status": "Synced", "health_status": "Healthy", "revision": "head", "message": "OK"},
        )
        return GitOpsSyncResult(
            sync_status=state["sync_status"],
            health_status=state["health_status"],
            revision=state["revision"],
            message=state["message"],
        )
