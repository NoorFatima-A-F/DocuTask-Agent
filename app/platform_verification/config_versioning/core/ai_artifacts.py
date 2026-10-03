"""
AI Artifact Version Manager (Models, System Prompts, RAG Configurations, Agents).
"""
from typing import Dict, List, Optional
from app.platform_verification.config_versioning.domain.models import (
    AIModelMetadata, PromptTemplateVersion, RAGRetrievalConfigVersion, AgentConfigVersion
)

class AIArtifactVersionManager:
    def __init__(self):
        self._prompts: Dict[str, Dict[str, PromptTemplateVersion]] = {}
        self._rag_configs: Dict[str, RAGRetrievalConfigVersion] = {}
        self._agent_configs: Dict[str, AgentConfigVersion] = {}
        self._load_defaults()

    def _load_defaults(self):
        p1 = PromptTemplateVersion(
            name="system_extraction_prompt",
            semantic_version="1.0.0",
            raw_prompt="You are an enterprise document extraction agent. Extract structured schema with 100% fidelity."
        )
        self.register_prompt(p1)

    def register_prompt(self, prompt: PromptTemplateVersion) -> PromptTemplateVersion:
        if prompt.name not in self._prompts:
            self._prompts[prompt.name] = {}
        self._prompts[prompt.name][prompt.semantic_version] = prompt
        return prompt

    def get_prompt(self, name: str, version: str = "1.0.0") -> Optional[PromptTemplateVersion]:
        return self._prompts.get(name, {}).get(version)

    def list_prompts(self) -> List[PromptTemplateVersion]:
        all_prompts = []
        for v_dict in self._prompts.values():
            all_prompts.extend(v_dict.values())
        return all_prompts

    def register_rag_config(self, config: RAGRetrievalConfigVersion) -> RAGRetrievalConfigVersion:
        self._rag_configs[config.config_id] = config
        return config

    def register_agent_config(self, config: AgentConfigVersion) -> AgentConfigVersion:
        self._agent_configs[config.agent_id] = config
        return config

ai_artifact_manager = AIArtifactVersionManager()
