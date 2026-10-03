# Configuration Distribution & Rollback Guide

## Versioned Configuration Bundles
All configurations deployed to clusters or regions are packaged into immutable `ConfigBundle` structures with SHA-256 integrity checksums.

## Deploying and Rolling Back Configurations
```python
from app.infrastructure.control_plane.config.distributor import ConfigurationDistributor

distributor = ConfigurationDistributor()

# Publish bundle
bundle_v1 = distributor.create_bundle(
    version="v1.2.0",
    payload={"log_level": "INFO", "max_concurrency": 64},
)

# Apply to cluster
distributor.distribute_to_cluster(bundle_v1.bundle_id, "cls-us-east-1a")

# Instant Rollback
distributor.rollback_cluster("cls-us-east-1a", "cfg_v1.1.0_priorchecksum")
```
