"""Notification Channels and Types."""

from enum import Enum


class NotificationChannel(str, Enum):
    IN_APP = "IN_APP"
    EMAIL = "EMAIL"
    SLACK = "SLACK"
    TEAMS = "TEAMS"
    WEBHOOK = "WEBHOOK"
    SMS = "SMS"


class NotificationEventType(str, Enum):
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    REVIEW_ASSIGNED = "REVIEW_ASSIGNED"
    REVIEW_ESCALATED = "REVIEW_ESCALATED"
    DECISION_SUBMITTED = "DECISION_SUBMITTED"
    HUMAN_OVERRIDE_EXECUTED = "HUMAN_OVERRIDE_EXECUTED"
    SLA_WARNING = "SLA_WARNING"
