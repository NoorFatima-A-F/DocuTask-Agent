# ADR-040: Pluggable Authentication Framework & Token Lifecycle

## Status
Accepted

## Context
External systems demand heterogeneous authentication mechanisms: OAuth2 with PKCE, API keys, JWT assertions, Bearer tokens, Basic Auth, mTLS, and cloud service accounts. Handling authentication ad-hoc across integrations causes token expiration failures and security vulnerabilities.

## Decision
We implement a centralized `AuthenticationManager` supporting all standard enterprise authentication flows. The framework manages automated token validation, OAuth2 refresh flows, header synthesis, and credential health monitoring without exposing raw secrets to client code.

## Consequences
- Single point of enforcement for token lifetimes, rotation, and header construction.
- Automated handling of 401 token refresh loops prevents unnecessary workflow interruptions.
- Simplifies connector plugin development by abstracting protocol negotiation.
