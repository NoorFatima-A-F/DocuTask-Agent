/**
 * Phase 13.21 - Enterprise AI Knowledge & Context Intelligence Platform (EAKCIP) Frontend Types
 */

export type KnowledgeLifecycleState =
  | 'DISCOVERED'
  | 'INGESTED'
  | 'PROCESSED'
  | 'INDEXED'
  | 'AVAILABLE'
  | 'UPDATED'
  | 'ARCHIVED';

export type SecurityClassification =
  | 'PUBLIC'
  | 'INTERNAL'
  | 'CONFIDENTIAL'
  | 'RESTRICTED'
  | 'STRICT_SECRET';

export type KnowledgeSourceType =
  | 'LOCAL_DOCUMENT'
  | 'GOOGLE_DRIVE'
  | 'SHAREPOINT'
  | 'SLACK'
  | 'TEAMS'
  | 'JIRA'
  | 'SALESFORCE'
  | 'GITHUB'
  | 'CONFLUENCE'
  | 'DATABASE';

export type EntityType =
  | 'EMPLOYEE'
  | 'DEPARTMENT'
  | 'PROJECT'
  | 'AI_AGENT'
  | 'SYSTEM'
  | 'POLICY'
  | 'DOCUMENT'
  | 'CONTRACT'
  | 'VENDOR'
  | 'CONCEPT';

export type MemoryTier =
  | 'SHORT_TERM'
  | 'LONG_TERM'
  | 'ORGANIZATIONAL'
  | 'PROCEDURAL';

export interface AccessPolicy {
  allowed_roles: string[];
  allowed_users: string[];
  denied_roles: string[];
  require_mfa: boolean;
  max_security_clearance: SecurityClassification;
}

export interface KnowledgeMetadata {
  author?: string;
  created_at: string;
  updated_at: string;
  file_type: string;
  file_size_bytes: number;
  token_count: number;
  custom_tags: string[];
  extracted_entities: string[];
  source_url?: string;
}

export interface KnowledgeAsset {
  id: string;
  tenant_id: string;
  organization_id: string;
  workspace_id: string;
  project_id: string;
  name: string;
  description: string;
  source_type: KnowledgeSourceType;
  source_id?: string;
  state: KnowledgeLifecycleState;
  security_classification: SecurityClassification;
  access_policy: AccessPolicy;
  raw_content: string;
  processed_content: string;
  embedding_ids: string[];
  metadata: KnowledgeMetadata;
  version: number;
  freshness_score: number;
  reliability_score: number;
  created_at: string;
  updated_at: string;
}

export interface KnowledgeSource {
  id: string;
  tenant_id: string;
  organization_id: string;
  workspace_id: string;
  name: string;
  source_type: KnowledgeSourceType;
  connection_config: Record<string, any>;
  sync_schedule: string;
  is_active: boolean;
  last_synced_at?: string;
  total_assets_synced: number;
  health_status: string;
  created_at: string;
}

export interface GraphNode {
  id: string;
  tenant_id: string;
  name: string;
  entity_type: EntityType;
  properties: Record<string, any>;
  confidence_score: number;
  created_at: string;
}

export interface GraphEdge {
  id: string;
  tenant_id: string;
  source_node_id: string;
  target_node_id: string;
  relation_type: string;
  properties: Record<string, any>;
  weight: number;
  created_at: string;
}

export interface RetrievedSnippet {
  asset_id: string;
  title: string;
  content: string;
  score: number;
  source_type: KnowledgeSourceType;
  security_classification: SecurityClassification;
  matched_via: string;
}

export interface ContextRetrievalResponse {
  query: string;
  snippets: RetrievedSnippet[];
  graph_context: string[];
  memory_context: string[];
  optimized_context_prompt: string;
  total_tokens_estimated: number;
  compression_ratio: number;
  retrieval_latency_ms: number;
}

export interface MemoryEntry {
  id: string;
  tenant_id: string;
  agent_id?: string;
  tier: MemoryTier;
  key: string;
  content: string;
  metadata: Record<string, any>;
  importance_score: number;
  access_count: number;
  expires_at?: string;
  created_at: string;
}

export interface KnowledgeConflict {
  id: string;
  tenant_id: string;
  asset_id_a: string;
  asset_id_b: string;
  conflict_topic: string;
  statement_a: string;
  statement_b: string;
  severity: string;
  detected_at: string;
  status: string;
  recommended_resolution: string;
}

export interface KnowledgeQualityReport {
  tenant_id: string;
  total_assets: number;
  freshness_index: number;
  avg_reliability_score: number;
  duplicate_assets_count: number;
  active_conflicts: KnowledgeConflict[];
  coverage_score: number;
  healthy: boolean;
}
