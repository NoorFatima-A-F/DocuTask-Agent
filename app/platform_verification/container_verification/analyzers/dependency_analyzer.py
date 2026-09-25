"""
Software Bill of Materials (SBOM) and Dependency Analyzer.
"""
import hashlib
from typing import List, Dict
from app.platform_verification.container_verification.models.verification_models import SbomPackage, SbomReport


class DependencyAnalyzer:
    """Generates SBOM and verifies package licenses and trusted registries."""

    FORBIDDEN_LICENSES = {"GPL-3.0", "AGPL-3.0", "UNKNOWN"}

    def generate_sbom(self, dependencies: List[Dict[str, str]]) -> SbomReport:
        packages: List[SbomPackage] = []
        untrusted: List[str] = []
        license_clean = True

        for dep in dependencies:
            name = dep.get("name", "package")
            version = dep.get("version", "1.0.0")
            lic = dep.get("license", "Apache-2.0")
            source = dep.get("source", "pypi")

            if lic in self.FORBIDDEN_LICENSES:
                license_clean = False
                untrusted.append(f"{name} ({lic})")

            if source not in ["pypi", "official", "internal-registry"]:
                untrusted.append(f"{name} from untrusted source '{source}'")

            pkg_hash = hashlib.sha256(f"{name}=={version}".encode()).hexdigest()
            packages.append(
                SbomPackage(
                    name=name,
                    version=version,
                    license_type=lic,
                    purl=f"pkg:pypi/{name}@{version}",
                    sha256_hash=pkg_hash,
                )
            )

        return SbomReport(
            total_packages=len(packages),
            packages=packages,
            untrusted_packages=untrusted,
            license_compliance_passed=license_clean and len(untrusted) == 0,
        )
