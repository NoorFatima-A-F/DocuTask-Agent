"""Test Teams, Memberships, and Invitation System."""

from app.tenancy.core.models import MembershipRole, InvitationState
from app.tenancy.teams.team_manager import TeamManager
from app.tenancy.teams.membership_manager import MembershipManager
from app.tenancy.teams.invitation_manager import InvitationManager


def test_team_and_membership_rbac():
    """Verify team membership and RBAC permissions."""
    team_mgr = TeamManager()
    mem_mgr = MembershipManager()

    team = team_mgr.create_team(
        team_id="team_eng_1",
        organization_id="org_1",
        name="AI Platform Core",
        department="Engineering",
        member_ids=["user_1", "user_2"],
    )
    assert len(team.member_ids) == 2

    # Assign Admin Role to user_1
    mem_mgr.assign_membership(
        membership_id="mem_1",
        user_id="user_1",
        organization_id="org_1",
        workspace_id="ws_main",
        role=MembershipRole.ADMIN,
    )

    # Assign Viewer Role to user_2
    mem_mgr.assign_membership(
        membership_id="mem_2",
        user_id="user_2",
        organization_id="org_1",
        workspace_id="ws_main",
        role=MembershipRole.VIEWER,
    )

    # user_1 (Admin) can write workflows
    assert mem_mgr.has_permission("user_1", "org_1", "workflow:write", "ws_main") is True
    # user_2 (Viewer) cannot write workflows
    assert mem_mgr.has_permission("user_2", "org_1", "workflow:write", "ws_main") is False
    # user_2 (Viewer) can read workflows
    assert mem_mgr.has_permission("user_2", "org_1", "workflow:read", "ws_main") is True


def test_invitation_lifecycle():
    """Verify 5-state invitation workflow."""
    inv_mgr = InvitationManager()

    inv = inv_mgr.create_invitation(
        invitation_id="inv_bob",
        email="bob@example.com",
        organization_id="org_1",
        inviter_user_id="user_admin",
        role=MembershipRole.MEMBER,
    )
    assert inv.status == InvitationState.CREATED

    inv_mgr.mark_sent(inv.invitation_id)
    assert inv.status == InvitationState.SENT

    accepted_inv = inv_mgr.accept_invitation(inv.token)
    assert accepted_inv.status == InvitationState.ACCEPTED

    activated_inv = inv_mgr.activate_invitation(inv.invitation_id)
    assert activated_inv.status == InvitationState.ACTIVE
