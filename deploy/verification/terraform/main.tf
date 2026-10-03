# Terraform Configuration for GCP Cloud Run and Storage
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

resource "google_cloud_run_v2_service" "verification_platform" {
  name     = "docutask-verification-platform"
  location = "us-central1"

  template {
    containers {
      image = "gcr.io/docutask-enterprise/verification-platform:latest"
      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
      }
    }
  }
}

resource "google_storage_bucket" "verification_evidence_cas" {
  name          = "docutask-verification-evidence-cas-prod"
  location      = "US"
  force_destroy = false
  versioning {
    enabled = true
  }
}
