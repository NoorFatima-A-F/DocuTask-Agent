"""
Platform Universal Constants.
Contains only universal time formats, MIME types, hash algorithms, encodings, and SemVer patterns.
Zero business constants allowed here.
"""
ISO_8601_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
UTC_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%SZ"

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 1000

MIME_JSON = "application/json"
MIME_YAML = "application/x-yaml"
MIME_OCTET_STREAM = "application/octet-stream"
MIME_TEXT_PLAIN = "text/plain"
MIME_PDF = "application/pdf"
MIME_PNG = "image/png"

HASH_SHA256 = "SHA-256"
HASH_SHA512 = "SHA-512"
HMAC_SHA256 = "HMAC-SHA256"

ENCODING_UTF8 = "utf-8"
ENCODING_ASCII = "ascii"
ENCODING_BASE64 = "base64"

SEMVER_REGEX_PATTERN = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
