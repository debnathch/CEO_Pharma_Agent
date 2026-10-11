# ADR-006: PostgreSQL Target with SQLite Local Development Storage

## Status
Accepted

## Context
The platform requires relational persistence for execution logs, evaluation runs, user feedback, improvement proposals, and audit events. Production enterprise deployments target PostgreSQL, but local developers and automated CI pipelines benefit from zero-configuration local storage without mandating a running Docker PostgreSQL container.

## Decision
We use **SQLAlchemy 2.x** with declarative ORM models and configure database connectivity via `DATABASE_URL`:
- Default Local Dev / Test: `sqlite:///./data/pharma.db` (or in-memory for ephemeral tests).
- Production Target: `postgresql+psycopg://user:pass@host:5432/pharma_db`.
Alembic migration scripts and model definitions are kept compatible across both dialects.

## Alternatives Considered
1. **PostgreSQL-only with mandatory Docker Compose**:
   - *Rejected*: Adds setup friction for local developers and interview reviewers running directly on native OS.
2. **NoSQL Document Database (MongoDB / DynamoDB)**:
   - *Rejected*: Lacks strong transactional consistency, schema integrity, and foreign key relations needed for audit and improvement governance.

## Consequences & Trade-offs
- **Positive**:
  - Instant zero-dependency setup on macOS, Linux, and Windows.
  - Seamless migration to PostgreSQL in production by setting one environment variable.
- **Negative / Trade-offs**:
  - Developers must avoid SQLite-incompatible SQL extensions when writing complex queries.
