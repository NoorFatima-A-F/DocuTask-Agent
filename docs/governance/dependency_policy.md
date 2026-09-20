# Dependency Governance & Supply Chain Security Policy

1. Standard library first. Avoid external libraries when simple implementations suffice.
2. No third-party framework (FastAPI, SQLAlchemy, Redis) may enter `app/shared_kernel/`.
3. Permitted licenses: MIT, Apache-2.0, BSD-3-Clause, ISC.
4. Pin all top-level dependencies.
