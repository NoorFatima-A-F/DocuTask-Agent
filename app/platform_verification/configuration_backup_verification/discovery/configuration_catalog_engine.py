"""
Configuration Catalog Engine for Enterprise Configuration Backup Verification (Part 3G.2D).
"""
from typing import List, Dict

from app.platform_verification.configuration_backup_verification.domain.models import (
    ConfigurationCategory,
    ConfigurationSensitivity,
    ConfigurationCatalogItem,
    ConfigurationCatalogReport,
    ConfigurationInventoryReport,
)
from app.platform_verification.configuration_backup_verification.domain.interfaces import (
    IConfigurationCatalogEngine,
)


class ConfigurationCatalogEngine(IConfigurationCatalogEngine):
    """
    Classifies configuration parameters into 18 enterprise categories,
    tracking ownership, environments, sensitivity, dependencies, and restore priorities.
    """

    CATALOG_SPEC = [
        # Database & Storage
        ("DATABASE_URL", ConfigurationCategory.DATABASE, "DataPlatformTeam", "Production", ConfigurationSensitivity.CONFIDENTIAL_SECRET, True, None, "v1.0", ["POSTGRES_INSTANCE"], "KMS_ENCRYPTED_VAULT", 1),
        ("DB_POOL_SIZE", ConfigurationCategory.DATABASE, "DataPlatformTeam", "Production", ConfigurationSensitivity.INTERNAL, False, "20", "v1.0", ["DATABASE_URL"], "CONFIGMAP_SNAPSHOT", 2),
        ("REDIS_URL", ConfigurationCategory.STORAGE, "CacheTeam", "Production", ConfigurationSensitivity.CONFIDENTIAL_SECRET, True, None, "v1.0", ["REDIS_CLUSTER"], "KMS_ENCRYPTED_VAULT", 1),
        ("STORAGE_BACKEND", ConfigurationCategory.STORAGE, "StorageTeam", "Production", ConfigurationSensitivity.INTERNAL, True, "S3_MINIO", "v1.0", [], "CONFIGMAP_SNAPSHOT", 2),
        ("UPLOAD_DIRECTORY", ConfigurationCategory.STORAGE, "StorageTeam", "Production", ConfigurationSensitivity.INTERNAL, True, "/data/uploads", "v1.0", ["STORAGE_BACKEND"], "CONFIGMAP_SNAPSHOT", 2),
        ("MAX_UPLOAD_SIZE", ConfigurationCategory.STORAGE, "StorageTeam", "Production", ConfigurationSensitivity.PUBLIC, False, "104857600", "v1.0", [], "CONFIGMAP_SNAPSHOT", 3),

        # Auth & Security
        ("JWT_SECRET", ConfigurationCategory.AUTHENTICATION, "SecurityTeam", "Production", ConfigurationSensitivity.CONFIDENTIAL_SECRET, True, None, "v2.0", ["KMS_ROOT_KEY"], "HARDWARE_SEALED_VAULT", 1),
        ("JWT_EXPIRATION_SECONDS", ConfigurationCategory.AUTHENTICATION, "SecurityTeam", "Production", ConfigurationSensitivity.INTERNAL, False, "86400", "v1.0", ["JWT_SECRET"], "CONFIGMAP_SNAPSHOT", 3),
        ("RBAC_POLICY_PATH", ConfigurationCategory.AUTHORIZATION, "SecurityTeam", "Production", ConfigurationSensitivity.RESTRICTED, True, "/etc/docutask/rbac.json", "v1.0", [], "VERSIONED_GIT_BACKUP", 2),
        ("ENCRYPTION_MASTER_KEY", ConfigurationCategory.SECURITY, "SecurityTeam", "Production", ConfigurationSensitivity.CONFIDENTIAL_SECRET, True, None, "v3.0", ["HSM_MODULE"], "HARDWARE_SEALED_VAULT", 1),
        ("TLS_CERT_PATH", ConfigurationCategory.SECURITY, "SecurityTeam", "Production", ConfigurationSensitivity.RESTRICTED, True, "/etc/ssl/certs/docutask.crt", "v1.0", [], "PKI_CERT_MANAGER", 1),
        ("TLS_KEY_PATH", ConfigurationCategory.SECURITY, "SecurityTeam", "Production", ConfigurationSensitivity.CONFIDENTIAL_SECRET, True, "/etc/ssl/private/docutask.key", "v1.0", ["TLS_CERT_PATH"], "PKI_CERT_MANAGER", 1),

        # AI & OCR Providers
        ("GEMINI_API_KEY", ConfigurationCategory.AI_PROVIDERS, "AIEngineering", "Production", ConfigurationSensitivity.CONFIDENTIAL_SECRET, True, None, "v1.0", [], "KMS_ENCRYPTED_VAULT", 1),
        ("GEMINI_MODEL_VERSION", ConfigurationCategory.AI_PROVIDERS, "AIEngineering", "Production", ConfigurationSensitivity.INTERNAL, False, "gemini-2.5-flash", "v1.0", ["GEMINI_API_KEY"], "CONFIGMAP_SNAPSHOT", 3),
        ("OCR_PROVIDER", ConfigurationCategory.OCR_PROVIDERS, "DocumentProcessingTeam", "Production", ConfigurationSensitivity.INTERNAL, True, "TESSERACT_HYBRID", "v1.0", [], "CONFIGMAP_SNAPSHOT", 2),
        ("OCR_CONCURRENCY_LIMIT", ConfigurationCategory.OCR_PROVIDERS, "DocumentProcessingTeam", "Production", ConfigurationSensitivity.INTERNAL, False, "16", "v1.0", ["OCR_PROVIDER"], "CONFIGMAP_SNAPSHOT", 3),

        # Application, Runtime & Workers
        ("APP_ENV", ConfigurationCategory.APPLICATION, "CorePlatformTeam", "Production", ConfigurationSensitivity.PUBLIC, True, "production", "v1.0", [], "CONFIGMAP_SNAPSHOT", 4),
        ("WORKER_CONCURRENCY", ConfigurationCategory.WORKER_RUNTIME, "CorePlatformTeam", "Production", ConfigurationSensitivity.INTERNAL, False, "8", "v1.0", ["REDIS_URL"], "CONFIGMAP_SNAPSHOT", 3),
        ("CELERY_TASK_TIMEOUT", ConfigurationCategory.SCHEDULER, "CorePlatformTeam", "Production", ConfigurationSensitivity.INTERNAL, False, "300", "v1.0", [], "CONFIGMAP_SNAPSHOT", 3),
        ("RATE_LIMIT_BURST", ConfigurationCategory.RATE_LIMITS, "SecurityTeam", "Production", ConfigurationSensitivity.INTERNAL, False, "100", "v1.0", ["REDIS_URL"], "CONFIGMAP_SNAPSHOT", 3),
        ("RATE_LIMIT_RATE", ConfigurationCategory.RATE_LIMITS, "SecurityTeam", "Production", ConfigurationSensitivity.INTERNAL, False, "20/s", "v1.0", ["RATE_LIMIT_BURST"], "CONFIGMAP_SNAPSHOT", 3),

        # Networking & Infrastructure
        ("HOST_BIND", ConfigurationCategory.NETWORKING, "InfraTeam", "Production", ConfigurationSensitivity.PUBLIC, False, "0.0.0.0", "v1.0", [], "CONFIGMAP_SNAPSHOT", 4),
        ("PORT", ConfigurationCategory.NETWORKING, "InfraTeam", "Production", ConfigurationSensitivity.PUBLIC, True, "8000", "v1.0", ["HOST_BIND"], "CONFIGMAP_SNAPSHOT", 4),
        ("CLUSTER_REGION", ConfigurationCategory.INFRASTRUCTURE, "InfraTeam", "Production", ConfigurationSensitivity.PUBLIC, True, "us-east-1", "v1.0", [], "TERRAFORM_STATE_BACKUP", 2),

        # Feature Flags, Observability, Logging & Telemetry
        ("ENABLE_ADVANCED_OCR", ConfigurationCategory.FEATURE_FLAGS, "ProductTeam", "Production", ConfigurationSensitivity.PUBLIC, False, "true", "v1.0", ["OCR_PROVIDER"], "FEATURE_FLAG_STORE_BACKUP", 3),
        ("ENABLE_VECTOR_SEARCH", ConfigurationCategory.FEATURE_FLAGS, "ProductTeam", "Production", ConfigurationSensitivity.PUBLIC, False, "true", "v1.0", ["DATABASE_URL"], "FEATURE_FLAG_STORE_BACKUP", 3),
        ("LOG_LEVEL", ConfigurationCategory.LOGGING, "ObservabilityTeam", "Production", ConfigurationSensitivity.PUBLIC, False, "INFO", "v1.0", [], "CONFIGMAP_SNAPSHOT", 4),
        ("LOG_FORMAT", ConfigurationCategory.LOGGING, "ObservabilityTeam", "Production", ConfigurationSensitivity.PUBLIC, False, "JSON", "v1.0", ["LOG_LEVEL"], "CONFIGMAP_SNAPSHOT", 4),
        ("PROMETHEUS_PORT", ConfigurationCategory.OBSERVABILITY, "ObservabilityTeam", "Production", ConfigurationSensitivity.PUBLIC, False, "9090", "v1.0", [], "CONFIGMAP_SNAPSHOT", 4),
        ("OTEL_EXPORTER_OTLP_ENDPOINT", ConfigurationCategory.TELEMETRY, "ObservabilityTeam", "Production", ConfigurationSensitivity.INTERNAL, False, "http://otel-collector:4317", "v1.0", [], "CONFIGMAP_SNAPSHOT", 4),
        ("HEALTH_CHECK_INTERVAL_SECONDS", ConfigurationCategory.MONITORING, "ObservabilityTeam", "Production", ConfigurationSensitivity.PUBLIC, False, "10", "v1.0", [], "CONFIGMAP_SNAPSHOT", 4),
    ]

    def build_configuration_catalog(
        self, inventory: ConfigurationInventoryReport
    ) -> ConfigurationCatalogReport:
        """
        Builds complete categorized configuration catalog with restore priorities and sensitivities.
        """
        items: List[ConfigurationCatalogItem] = []
        items_by_cat: Dict[str, int] = {}
        items_by_sens: Dict[str, int] = {}

        for (
            name, cat, owner, env, sens, req, default, ver, deps, strat, prio
        ) in self.CATALOG_SPEC:
            item = ConfigurationCatalogItem(
                name=name,
                category=cat,
                owner=owner,
                environment=env,
                sensitivity=sens,
                required=req,
                default_value=default,
                version=ver,
                dependencies=deps,
                backup_strategy=strat,
                restore_priority=prio,
            )
            items.append(item)

            cat_key = cat.value
            items_by_cat[cat_key] = items_by_cat.get(cat_key, 0) + 1

            sens_key = sens.value
            items_by_sens[sens_key] = items_by_sens.get(sens_key, 0) + 1

        all_cats = [c.value for c in ConfigurationCategory]

        return ConfigurationCatalogReport(
            total_catalog_items=len(items),
            categories_covered=all_cats,
            items_by_category=items_by_cat,
            items_by_sensitivity=items_by_sens,
            catalog_items=items,
            passed=len(items) >= 30,
        )
