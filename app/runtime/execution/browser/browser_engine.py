"""
Browser Automation & Vision Engine for Phase 13.15.
Manages headless browser sessions, DOM tree extractions, vision snapshots, and synthetic interaction scripts.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.execution.events.execution_events import (
    ExecutionEvent,
    ExecutionEventType,
    RiskLevel,
    execution_event_bus,
)


@dataclass
class BrowserAction:
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action_type: str = "navigate"  # navigate, click, fill, select, press_key, scroll, screenshot, evaluate_js
    selector: Optional[str] = None
    value: Optional[str] = None
    timeout_ms: int = 10000
    status: str = "pending"  # pending, executed, failed
    result_data: Optional[Dict[str, Any]] = None
    screenshot_ref: Optional[str] = None
    executed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "selector": self.selector,
            "value": self.value,
            "timeout_ms": self.timeout_ms,
            "status": self.status,
            "result_data": self.result_data,
            "screenshot_ref": self.screenshot_ref,
            "executed_at": self.executed_at,
        }


@dataclass
class BrowserSession:
    session_id: str
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    viewport_width: int = 1920
    viewport_height: int = 1080
    current_url: str = "about:blank"
    page_title: str = "Blank"
    dom_elements_count: int = 0
    cookies_count: int = 0
    actions: List[BrowserAction] = field(default_factory=list)
    is_active: bool = True
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_activity: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "user_agent": self.user_agent,
            "viewport_width": self.viewport_width,
            "viewport_height": self.viewport_height,
            "current_url": self.current_url,
            "page_title": self.page_title,
            "dom_elements_count": self.dom_elements_count,
            "cookies_count": self.cookies_count,
            "actions_count": len(self.actions),
            "is_active": self.is_active,
            "created_at": self.created_at,
            "last_activity": self.last_activity,
        }


class BrowserEngine:
    """Headless browser orchestration and DOM-vision grounding engine."""

    def __init__(self):
        self._sessions: Dict[str, BrowserSession] = {}
        self._initialize_seed_sessions()

    def _initialize_seed_sessions(self) -> None:
        seed = BrowserSession(
            session_id="browser_session_portal_audit",
            current_url="https://portal.enterprise-vendor.com/invoices",
            page_title="Vendor Billing & Invoices Management",
            dom_elements_count=428,
            cookies_count=6,
            actions=[
                BrowserAction(
                    action_type="navigate",
                    value="https://portal.enterprise-vendor.com/login",
                    status="executed",
                    executed_at=datetime.now(timezone.utc).isoformat(),
                    result_data={"http_status": 200, "page_title": "Vendor Login"},
                ),
                BrowserAction(
                    action_type="fill",
                    selector="input#username",
                    value="ai-automation-bot@enterprise.corp",
                    status="executed",
                    executed_at=datetime.now(timezone.utc).isoformat(),
                ),
                BrowserAction(
                    action_type="click",
                    selector="button.btn-primary-login",
                    status="executed",
                    executed_at=datetime.now(timezone.utc).isoformat(),
                    result_data={"redirect_url": "https://portal.enterprise-vendor.com/invoices"},
                ),
                BrowserAction(
                    action_type="screenshot",
                    status="executed",
                    screenshot_ref="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
                    executed_at=datetime.now(timezone.utc).isoformat(),
                ),
            ],
        )
        self._sessions[seed.session_id] = seed

    def create_session(
        self,
        session_id: Optional[str] = None,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
    ) -> BrowserSession:
        sid = session_id or f"session_{uuid.uuid4().hex[:10]}"
        session = BrowserSession(
            session_id=sid,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
        )
        self._sessions[sid] = session
        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.BROWSER_SESSION_STARTED,
                source="browser_engine",
                payload={"session_id": sid, "viewport": f"{viewport_width}x{viewport_height}"},
            )
        )
        return session

    def get_session(self, session_id: str) -> Optional[BrowserSession]:
        return self._sessions.get(session_id)

    def list_sessions(self) -> List[BrowserSession]:
        return list(self._sessions.values())

    def execute_action(
        self,
        session_id: str,
        action_type: str,
        selector: Optional[str] = None,
        value: Optional[str] = None,
    ) -> Dict[str, Any]:
        session = self.get_session(session_id)
        if not session:
            session = self.create_session(session_id=session_id)

        now = datetime.now(timezone.utc).isoformat()
        action = BrowserAction(
            action_type=action_type,
            selector=selector,
            value=value,
            executed_at=now,
        )

        # Process synthetic browser operation
        if action_type == "navigate":
            session.current_url = value or "https://example.com"
            session.page_title = f"Dashboard - {session.current_url.split('//')[-1].split('/')[0]}"
            session.dom_elements_count = 350
            action.status = "executed"
            action.result_data = {
                "url": session.current_url,
                "status_code": 200,
                "title": session.page_title,
                "ssl_verified": True,
            }
            execution_event_bus.publish(
                ExecutionEvent(
                    event_type=ExecutionEventType.BROWSER_NAVIGATED,
                    source="browser_engine",
                    payload={"session_id": session_id, "url": session.current_url},
                )
            )
        elif action_type == "screenshot":
            action.status = "executed"
            # Synthetic 1x1 base64 png
            action.screenshot_ref = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            action.result_data = {"format": "png", "width": session.viewport_width, "height": session.viewport_height}
            execution_event_bus.publish(
                ExecutionEvent(
                    event_type=ExecutionEventType.BROWSER_SCREENSHOT_CAPTURED,
                    source="browser_engine",
                    payload={"session_id": session_id, "url": session.current_url},
                )
            )
        elif action_type in ["click", "fill", "select", "press_key", "scroll"]:
            action.status = "executed"
            action.result_data = {"target_selector": selector, "applied_value": value, "elements_matched": 1}
            execution_event_bus.publish(
                ExecutionEvent(
                    event_type=ExecutionEventType.BROWSER_ACTION_PERFORMED,
                    source="browser_engine",
                    payload={"session_id": session_id, "action": action_type, "selector": selector},
                )
            )
        else:
            action.status = "executed"
            action.result_data = {"message": f"Action {action_type} executed"}

        session.actions.append(action)
        session.last_activity = now

        return {
            "success": True,
            "session_id": session.session_id,
            "action": action.to_dict(),
            "current_url": session.current_url,
            "page_title": session.page_title,
        }

    def close_session(self, session_id: str) -> bool:
        session = self.get_session(session_id)
        if session:
            session.is_active = False
            execution_event_bus.publish(
                ExecutionEvent(
                    event_type=ExecutionEventType.BROWSER_SESSION_CLOSED,
                    source="browser_engine",
                    payload={"session_id": session_id},
                )
            )
            return True
        return False


# Global Singleton
browser_engine = BrowserEngine()
