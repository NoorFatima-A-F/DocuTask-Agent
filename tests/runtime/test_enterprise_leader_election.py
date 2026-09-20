"""
Enterprise Leader Election Coordinator Test Suite.
Validates:
- Lease acquisition & exclusivity
- Rejection of competing candidates while lease is active
- Leader renewal and heartbeat maintenance
- Voluntary step down
- Automatic failover upon lease expiration
"""

import time
import pytest
from app.agents.runtime.enterprise.leader_election import LeaderElectionCoordinator


def test_leader_acquisition_and_exclusivity():
    coord = LeaderElectionCoordinator(lease_duration_seconds=5.0)

    # Node 1 acquires
    assert coord.try_acquire_leadership("node-1")
    assert coord.get_leader() == "node-1"

    # Node 2 tries -> rejected
    assert not coord.try_acquire_leadership("node-2")
    assert coord.get_leader() == "node-1"

    # Node 1 re-acquires (idempotent renewal)
    assert coord.try_acquire_leadership("node-1")


def test_leader_renewal():
    coord = LeaderElectionCoordinator(lease_duration_seconds=5.0)
    coord.try_acquire_leadership("node-1")

    # Node 1 renews
    assert coord.renew_leadership("node-1")

    # Node 2 cannot renew
    assert not coord.renew_leadership("node-2")


def test_leader_step_down():
    coord = LeaderElectionCoordinator(lease_duration_seconds=5.0)
    coord.try_acquire_leadership("node-1")

    # Node 2 cannot force step down
    assert not coord.step_down("node-2")
    assert coord.get_leader() == "node-1"

    # Node 1 steps down
    assert coord.step_down("node-1")
    assert coord.get_leader() is None

    # Now Node 2 can acquire
    assert coord.try_acquire_leadership("node-2")
    assert coord.get_leader() == "node-2"


def test_lease_expiration_and_failover():
    # Very short lease for test
    coord = LeaderElectionCoordinator(lease_duration_seconds=0.05)
    coord.try_acquire_leadership("node-1")
    assert coord.get_leader() == "node-1"

    # Wait for lease to expire
    time.sleep(0.07)
    assert coord.get_leader() is None

    # Node 2 takes over
    assert coord.try_acquire_leadership("node-2")
    assert coord.get_leader() == "node-2"


class MockRedisSync:
    def __init__(self):
        self.store = {}

    def set(self, key, val, nx=False, px=None):
        if nx and key in self.store:
            return None
        self.store[key] = val
        return True

    def get(self, key):
        return self.store.get(key)

    def delete(self, key):
        self.store.pop(key, None)


def test_redis_leader_election_provider():
    from app.agents.runtime.enterprise.leader_election import RedisLeaseProvider

    mock_redis = MockRedisSync()
    provider = RedisLeaseProvider(redis_sync_client=mock_redis)
    coord = LeaderElectionCoordinator(lease_duration_seconds=5.0, provider=provider)

    assert coord.try_acquire_leadership("node-redis-1")
    assert coord.get_leader() == "node-redis-1"

    # Competing node
    assert not coord.try_acquire_leadership("node-redis-2")

    # Renewal
    assert coord.renew_leadership("node-redis-1")

    # Step down
    assert coord.step_down("node-redis-1")
    assert coord.get_leader() is None


class MockPostgresSync:
    def __init__(self):
        self.rows = {}

    def execute_update(self, query, params):
        if "INSERT INTO runtime_leader_leases" in query:
            lease_name, candidate_id, expires, now, cand_id2 = params
            curr = self.rows.get(lease_name)
            if curr is None or curr["expires_at"] < now or curr["leader_id"] == candidate_id:
                self.rows[lease_name] = {"leader_id": candidate_id, "expires_at": expires}
                return 1
            return 0
        elif "UPDATE runtime_leader_leases" in query:
            expires, lease_name, leader_id, now = params
            curr = self.rows.get(lease_name)
            if curr and curr["leader_id"] == leader_id and curr["expires_at"] >= now:
                curr["expires_at"] = expires
                return 1
            return 0
        elif "DELETE FROM runtime_leader_leases" in query:
            lease_name, leader_id = params
            curr = self.rows.get(lease_name)
            if curr and curr["leader_id"] == leader_id:
                del self.rows[lease_name]
                return 1
            return 0
        return 0

    def fetch_one(self, query, params):
        lease_name = params[0]
        curr = self.rows.get(lease_name)
        if curr:
            return (curr["leader_id"], curr["expires_at"])
        return None


def test_postgres_leader_election_provider():
    from app.agents.runtime.enterprise.leader_election import PostgresAdvisoryLockProvider

    mock_db = MockPostgresSync()
    provider = PostgresAdvisoryLockProvider(db_sync_client=mock_db)
    coord = LeaderElectionCoordinator(lease_duration_seconds=5.0, provider=provider)

    assert coord.try_acquire_leadership("node-pg-1")
    assert coord.get_leader() == "node-pg-1"

    # Competing node fails
    assert not coord.try_acquire_leadership("node-pg-2")

    # Renewal
    assert coord.renew_leadership("node-pg-1")

    # Step down
    assert coord.step_down("node-pg-1")
    assert coord.get_leader() is None

