# Enterprise Security Architecture & Cryptographic Threat Model

**Platform Name**: AI Document Processing Platform  
**Target Path**: `C:\Users\User\Desktop\ai_document_processing_platform`  
**Document Status**: LOCKED (Foundation Release Baseline)  
**Security Baseline**: Enterprise OWASP Standards  

---

## 1. Authentication Architecture

The AI Document Processing Platform utilizes a stateless JSON Web Token (JWT) Access Token architecture paired with a database-backed, cryptographically hashed Refresh Token Rotation (RTR) mechanism.

```
                    ┌──────────────────────────────────────┐
                    │       POST /api/v1/auth/login        │
                    └──────────────────┬───────────────────┘
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │  Verify Credentials (Bcrypt Hash)     │
                   └──────────────────┬────────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
  Access Token (JWT HS256)                      Refresh Token (Raw UUID + JWT)
  - Short-Lived (30 mins)                        - Long-Lived (7 Days)
  - Stateless Bearer Header                      - Stored as SHA-256 Hash in DB
```

---

## 2. JWT Structure & Cryptographic Claims

Access and Refresh Tokens are signed using the `HS256` (HMAC-SHA256) algorithm with a 256-bit high-entropy secret (`JWT_SECRET`).

### JWT Payload Specification (RFC 7519 Compliant)
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "jti": "b0f745e7-6a12-4fbc-b5bc-69538356ecdf",
  "iat": 1776470400,
  "exp": 1776472200,
  "type": "access"
}
```

- `sub` (Subject): User UUID.
- `jti` (JWT ID): Unique, cryptographically random UUID v4 issued per token for collision-resistant tracking.
- `iat` (Issued At): UTC timestamp of token issuance.
- `exp` (Expiration): UTC timestamp of token expiration.
- `type` (Token Type): Hard-scoped token purpose (`access` or `refresh`). Prevents token misuse cross-submission.

---

## 3. Refresh Token Lifecycle & Rotation (RTR)

```
        Client Request (POST /auth/refresh)
                        │
                        ▼
       Hash Raw Token: SHA-256(refresh_token)
                        │
                        ▼
       Lookup DB Record: token_hash == SHA-256 AND revoked == False
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
    Record Found                 Not Found / Revoked
         │                             │
         ▼                             ▼
   Revoke Old Token           Reject Request (401 Unauthorized)
  (set revoked=True)                   │
         │                             ▼
         ▼                    Possible Replay Attack!
   Issue New Pair
 (Access + Refresh)
```

1. **Storage Security**: Raw refresh tokens are never persisted. Database stores `token_hash = SHA256(raw_token)`.
2. **Single-Use Rotation**: Using a refresh token immediately revokes its database record (`revoked = True`) and issues a new refresh token.
3. **Replay Protection**: Re-using a previously revoked refresh token fails DB validation and is rejected immediately.
4. **Session Termination**:
   - `POST /auth/logout`: Revokes the specific refresh token hash.
   - `POST /auth/logout-all`: Revokes **ALL** active refresh tokens owned by the user.
   - Password Update: Instantly revokes all active sessions owned by the user.

---

## 4. Role-Based Access Control (RBAC) Architecture

Authorization is enforced via FastAPI dependency injection:

- `get_current_active_user`: Ensures user is authenticated and `is_active == True`.
- `RoleChecker(allowed_roles)`: Verifies user possesses explicit roles (`admin`, `user`).
- `get_current_admin`: Specialized shorthand requiring `role == "admin"` or `is_superuser == True`.
- Multi-Tenant Isolation: Business services verify resource ownership (`doc.owner_id == owner.id`) before permitting read, update, or deletion operations.

---

## 5. Password Policy & Cryptography

- **Algorithm**: Bcrypt (`passlib.context.CryptContext` with automatic per-password salt generation).
- **Password Complexity Rules**:
  - Minimum length: 8 characters
  - Requires at least 1 uppercase letter (`A-Z`)
  - Requires at least 1 lowercase letter (`a-z`)
  - Requires at least 1 numeric digit (`0-9`)
  - Requires at least 1 special character (`!@#$%^&*()_+-=[]{}|;:,.<>?`)

---

## 6. Rate Limiting Architecture

Protects authentication routes via `RateLimitMiddleware` using a sliding window algorithm:

- `POST /api/v1/auth/login`: 5 requests / minute
- `POST /api/v1/auth/register`: 10 requests / minute
- `POST /api/v1/auth/refresh`: 20 requests / minute
- Failure Response: `429 Too Many Requests` formatted in standard `APIResponse` envelope.

---

## 7. OWASP Enterprise Security Response Headers

All HTTP responses automatically include OWASP-recommended security headers:

- `X-Frame-Options: DENY` (Clickjacking defense)
- `X-Content-Type-Options: nosniff` (MIME-sniffing defense)
- `X-XSS-Protection: 1; mode=block` (Cross-Site Scripting filter)
- `Referrer-Policy: strict-origin-when-cross-origin` (Referrer privacy)
- `Permissions-Policy: geolocation=(), camera=(), microphone=()` (API restrictions)
- `Content-Security-Policy: default-src 'self'; frame-ancestors 'none';` (Resource restrictions)
- `Cache-Control: no-store, max-age=0` (Sensitive API response caching prevention)

---

## 8. Threat Model & CSRF Assessment

- **CSRF Risk**: **NOT APPLICABLE**. Authentication tokens are delivered via custom `Authorization: Bearer <token>` HTTP headers. Browsers do not auto-attach custom authorization headers on cross-site requests (unlike ambient cookie storage), rendering CSRF attacks impossible.
- **XSS Mitigation**: Access tokens are recommended to be stored in transient client memory state. Token lifetime is restricted to 30 minutes.

---

## 9. Foundation Freeze Decision

The backend foundation is formally declared **FOUNDATION LOCKED**.

The following core modules are frozen:
- `app/core/` (config, security, logging, exceptions)
- `app/database/` (base, session)
- `app/middleware/` (exception_handler, request_context, rate_limit)
- `app/models/user.py` & `app/models/refresh_token.py`
- `app/dependencies/auth.py` & `app/dependencies/db.py`
- `Dockerfile` & `docker-compose.yml`

Future prompts MUST NOT alter these frozen foundation modules unless a Critical Severity security vulnerability is discovered.
