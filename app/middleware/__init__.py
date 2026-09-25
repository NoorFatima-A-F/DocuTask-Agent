"""
Middleware Package.
Contains global exception handling and unified API envelope formatting.
"""

from app.middleware.exception_handler import register_exception_handlers

__all__ = ["register_exception_handlers"]
