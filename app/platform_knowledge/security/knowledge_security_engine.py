"""
Knowledge Security Engine
RBAC/ABAC enforcement, security classification filtering, PII sanitization, and audit trails.
"""
import re
from typing import List
from ..models.schemas import SecurityClassification, KnowledgeAsset

class KnowledgeSecurityEngine:
    @staticmethod
    def mask_pii(text: str) -> str:
        # Mask emails
        text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[PII_EMAIL_MASKED]', text)
        # Mask SSN / Credit Card patterns
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[PII_SSN_MASKED]', text)
        text = re.sub(r'\b(?:\d{4}[ -]?){4}\b', '[PII_CARD_MASKED]', text)
        return text

    @staticmethod
    def audit_access_allowed(
        asset: KnowledgeAsset,
        user_clearance: SecurityClassification,
        user_roles: List[str]
    ) -> bool:
        clearance_hierarchy = {
            SecurityClassification.PUBLIC: 1,
            SecurityClassification.INTERNAL: 2,
            SecurityClassification.CONFIDENTIAL: 3,
            SecurityClassification.RESTRICTED: 4,
            SecurityClassification.STRICT_SECRET: 5,
        }
        user_level = clearance_hierarchy.get(user_clearance, 2)
        asset_level = clearance_hierarchy.get(asset.security_classification, 2)
        
        if asset_level > user_level:
            return False
            
        if asset.access_policy.allowed_roles:
            if not any(r in asset.access_policy.allowed_roles for r in user_roles):
                return False
                
        return True
