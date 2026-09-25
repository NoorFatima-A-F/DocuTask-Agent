"""Data Locality and Storage Proximity Resolver."""

import re
from typing import Optional


class DataLocalityResolver:
    """Resolves preferred regional and cluster locality from data storage URIs."""

    REGION_PATTERNS = {
        r"us-east-1": "us-east-1",
        r"us-west-2": "us-west-2",
        r"eu-west-1": "eu-west-1",
        r"eu-central-1": "eu-central-1",
        r"ap-southeast-1": "ap-southeast-1",
    }

    @classmethod
    def resolve_locality_region(cls, data_uri: Optional[str]) -> Optional[str]:
        """Extract region identifier from storage bucket or object URI."""
        if not data_uri:
            return None

        for pattern, region_id in cls.REGION_PATTERNS.items():
            if re.search(pattern, data_uri, re.IGNORECASE):
                return region_id

        return None
