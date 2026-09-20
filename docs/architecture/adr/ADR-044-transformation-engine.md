# ADR-044: Universal Transformation & Schema Mapping Engine

## Status
Accepted

## Context
Connecting disparate enterprise systems requires continuous data transformation across JSON, XML, CSV, YAML, and binary formats, as well as field-level renaming, type coercion, nested extraction, conditional logic, and enum lookup tables.

## Decision
We implement a two-tier transformation layer:
1. `TransformationEngine`: Handles low-level multi-format conversions (JSON, XML, CSV, YAML, Base64).
2. `SchemaMapper`: Executes declarative `SchemaMappingPlan` definitions with dot-path navigation, computed string templates, default fallbacks, custom value transforms, and lookup dictionaries.

## Consequences
- Declarative, version-controlled mappings eliminate custom Python glue scripts in workflows.
- Seamless bridging between legacy XML/SOAP backends and modern JSON REST/GraphQL services.
