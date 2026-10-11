# ADR-001: Modular Monolith vs Microservices Architecture

## Status
Accepted

## Context
Bengal Remedies requires an extensible multi-agent AI ecosystem to support executive decision-making across ethical sales, PCD distribution, billing, finance, logistics, procurement, and HR. Early-stage AI systems often suffer from premature distributed decomposition, introducing operational complexity (network latency, distributed transactions, message broker maintenance, service discovery) before agent domains, execution boundaries, and evaluation metrics stabilize.

## Decision
We implement the foundation platform as a **Modular Monolith** using Python 3.12, FastAPI, and Pydantic v2.
All business services, agent modules, orchestration engines, and persistence layers reside within a single codebase under strict package boundaries (`src/pharma_platform/*`). Communication between agents and shared business services occurs via in-process typed contracts (`BaseAgent`, `AgentRequest`, `AgentResult`).

## Alternatives Considered
1. **Microservices Architecture with gRPC / REST**:
   - *Rejected*: Massive operational overhead, distributed tracing complexity, serialization tax across agent calls, difficult local developer experience without Docker/Kubernetes.
2. **Event-Driven Microservices with Kafka / RabbitMQ**:
   - *Rejected*: Inappropriate for synchronous request-response CEO conversational queries and introduces eventual consistency issues into financial and inventory calculations.

## Consequences & Trade-offs
- **Positive**:
  - Extremely fast local startup and testing (0.4s for full test suite).
  - Single process execution simplifies debugging and local Ollama inference coordination.
  - Zero network overhead for inter-agent data passing.
  - Straightforward transaction boundaries and SQLite/PostgreSQL switching.
- **Negative / Trade-offs**:
  - All agents share the same runtime process; CPU-intensive operations must be managed asynchronously.
  - Scalability is vertical or through multiple monolith replicas behind a load balancer rather than per-agent fine-grained autoscaling.
