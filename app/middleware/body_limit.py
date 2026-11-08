"""Cap request body size while it streams in, before multipart parsing spools it to disk.

A declared ``Content-Length`` over the cap is rejected immediately; bodies without one
(chunked) are counted chunk by chunk and aborted with 413 as soon as they pass the cap.
"""

from __future__ import annotations

import json

from fastapi import HTTPException
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.config import settings

#: Non-upload endpoints only take small JSON bodies.
DEFAULT_LIMIT_BYTES = 1 * 1024 * 1024
#: Multipart framing overhead allowed on top of the file-size limit.
MULTIPART_OVERHEAD_BYTES = 64 * 1024
UPLOAD_PATH = f"{settings.API_V1_STR}/documents/upload"


def limit_for(path: str) -> int:
    if path.rstrip("/") == UPLOAD_PATH:
        return settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024 + MULTIPART_OVERHEAD_BYTES
    return DEFAULT_LIMIT_BYTES


def _too_large(limit: int) -> HTTPException:
    return HTTPException(status_code=413, detail=f"Request body exceeds {limit} bytes")


class BodySizeLimitMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        limit = limit_for(scope["path"])
        declared = dict(scope.get("headers") or []).get(b"content-length")
        if declared is not None and declared.isdigit() and int(declared) > limit:
            await self._reject(send, limit)
            return

        received = 0
        started = False

        async def limited_receive() -> Message:
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > limit:
                    raise _too_large(limit)
            return message

        async def tracking_send(message: Message) -> None:
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
            await send(message)

        try:
            await self.app(scope, limited_receive, tracking_send)
        except HTTPException as exc:
            if exc.status_code != 413 or started:
                raise
            await self._reject(send, limit)

    @staticmethod
    async def _reject(send: Send, limit: int) -> None:
        body = json.dumps(
            {"success": False, "message": f"Request body exceeds {limit} bytes", "data": None, "errors": None}
        ).encode()
        await send(
            {
                "type": "http.response.start",
                "status": 413,
                "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())],
            }
        )
        await send({"type": "http.response.body", "body": body})
