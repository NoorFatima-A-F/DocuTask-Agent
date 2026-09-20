"""
Enterprise Document Understanding Layer
Extracts entities, relationships, events, dates, and policy rules.
"""
import re
from typing import Dict, Any, List
from ..models.schemas import KnowledgeAsset, EntityType

class DocumentUnderstandingLayer:
    @staticmethod
    def extract_structured_intelligence(asset: KnowledgeAsset) -> Dict[str, Any]:
        text = asset.raw_content
        
        # 1. Entity Extraction
        entities = []
        # Look for capitalized keywords or standard roles
        for match in re.finditer(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', text):
            token = match.group(1)
            if len(token) > 3 and token not in ["Standard", "Contains", "Enterprise", "System"]:
                entities.append(token)
        
        # 2. Date / Expiry Extraction
        dates = re.findall(r'\b\d{4}-\d{2}-\d{2}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b', text)
        
        # 3. Policy / Responsibility Extraction
        policies = []
        for line in text.split("."):
            if any(k in line.lower() for k in ["policy", "guideline", "must", "required", "responsible", "sla"]):
                policies.append(line.strip())

        extracted = {
            "entities": list(set(entities))[:10],
            "dates": dates,
            "policies": policies[:5],
            "language": "en",
            "summary": text[:200] + "..." if len(text) > 200 else text
        }
        
        asset.metadata.extracted_entities = extracted["entities"]
        return extracted
