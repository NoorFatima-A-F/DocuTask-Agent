"""
Snapshot Compressor for Phase 13.4.
Compresses replay snapshot payloads for scalable storage.
"""

import zlib
import base64


class SnapshotCompressor:
    """
    Zlib compression helper for replay state payloads.
    """

    @staticmethod
    def compress(raw_text: str) -> str:
        compressed = zlib.compress(raw_text.encode("utf-8"))
        return base64.b64encode(compressed).decode("ascii")

    @staticmethod
    def decompress(compressed_base64: str) -> str:
        raw_bytes = base64.b64decode(compressed_base64.encode("ascii"))
        return zlib.decompress(raw_bytes).decode("utf-8")
