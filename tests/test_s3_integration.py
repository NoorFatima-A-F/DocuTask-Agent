"""S3StorageProvider through the real boto3/botocore stack.

``tests/fakes/s3.py`` replaces the client object entirely, so it cannot catch a wrong
parameter name, a bad header or a misread error shape. These tests build the provider the
way production does (``client=None`` -> ``boto3.client("s3", ...)``) and talk to either:

* moto's in-memory S3 (default; no network, no account, no cost), or
* a real S3-compatible endpoint when ``S3_INTEGRATION_ENDPOINT`` and ``S3_INTEGRATION_BUCKET``
  are set (MinIO, SeaweedFS, R2 ...), using the standard ``AWS_*`` credentials.
"""

from __future__ import annotations

import os
import uuid
from collections.abc import Iterator

import pytest

from app.core.exceptions import ValidationAppException
from app.storage.s3 import S3StorageProvider

REAL_ENDPOINT = os.environ.get("S3_INTEGRATION_ENDPOINT")
REAL_BUCKET = os.environ.get("S3_INTEGRATION_BUCKET")


@pytest.fixture
def storage(monkeypatch: pytest.MonkeyPatch) -> Iterator[S3StorageProvider]:
    prefix = f"it-{uuid.uuid4().hex[:8]}/"
    if REAL_ENDPOINT and REAL_BUCKET:
        yield S3StorageProvider(REAL_BUCKET, prefix, endpoint_url=REAL_ENDPOINT, region=os.environ.get("S3_REGION"))
        return
    moto = pytest.importorskip("moto")
    for name, value in {
        "AWS_ACCESS_KEY_ID": "testing",
        "AWS_SECRET_ACCESS_KEY": "testing",
        "AWS_DEFAULT_REGION": "us-east-1",
    }.items():
        monkeypatch.setenv(name, value)
    monkeypatch.delenv("AWS_SESSION_TOKEN", raising=False)
    monkeypatch.delenv("AWS_PROFILE", raising=False)
    with moto.mock_aws():
        import boto3

        boto3.client("s3", region_name="us-east-1").create_bucket(Bucket="docutask-it")
        yield S3StorageProvider("docutask-it", prefix, region="us-east-1")


async def test_round_trip_sets_type_and_encryption(storage: S3StorageProvider) -> None:
    stored, key, location = await storage.save(b"%PDF-1.7 integration", "Scan.PDF")
    assert key.endswith(stored) and stored.endswith(".pdf")
    assert location == f"s3://{storage.bucket}/{key}" and key.startswith(storage.prefix)
    head = storage.client.head_object(Bucket=storage.bucket, Key=key)
    assert head["ContentType"] == "application/pdf"
    assert head.get("ServerSideEncryption") == "AES256"
    assert await storage.read(key) == b"%PDF-1.7 integration"
    assert await storage.exists(key) is True
    deleted = await storage.delete(key)
    assert deleted is True
    assert await storage.exists(key) is False


async def test_missing_object_maps_to_the_app_error(storage: S3StorageProvider) -> None:
    with pytest.raises(ValidationAppException, match="does not exist"):
        await storage.read(f"{storage.prefix}2026/01/01/{uuid.uuid4().hex}.png")


async def test_bucket_is_reachable_and_a_missing_one_is_reported(storage: S3StorageProvider) -> None:
    assert await storage.check() is None
    missing = S3StorageProvider(f"missing-{uuid.uuid4().hex[:12]}", client=storage.client)
    problem = await missing.check()
    assert problem is not None and missing.bucket in problem
