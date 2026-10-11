# ADR-011: Agent Contract, Manifest, and Versioning Strategy

## Status
Accepted

## Context
As Bengal Remedies expands its pharmaceutical capabilities across ethical sales, supply chain, and marketing, new agents will be introduced over multiple phases. Adding a new agent must never require modifying unrelated existing agent modules or rewriting monolithic conditional statements inside the CEO Master Agent.

## Decision
We enforce a standardized **Agent Contract and Manifest Strategy**:
1. All agents inherit from `BaseAgent` and declare a static `AgentManifest`:
   - `agent_id`: Stable identifier (e.g. `ethical_sales`).
   - `version`: Semver string (e.g. `0.1.0`).
   - `capabilities`: List of `AgentCapability` objects with input/output schemas and `is_implemented` flags.
   - `required_permissions`: Security and access scopes.
2. Incomplete or planned capabilities must return honest `status="not_implemented"` rather than hallucinating answers.
3. The CEO Master Agent discovers capabilities dynamically via `AgentRegistry.find_by_capability()`, allowing new specialist agents to be onboarded without altering CEO business logic.

## Alternatives Considered
1. **Unstructured dictionary passing between agents**:
   - *Rejected*: Inevitably leads to runtime KeyError exceptions and untyped schema drift.
2. **Dynamic code imports via `__import__` or `eval()`**:
   - *Rejected*: Insecure and susceptible to arbitrary code execution vulnerabilities.

## Consequences & Trade-offs
- **Positive**:
  - Predictable onboarding lifecycle for new specialist agents.
  - Truthful capability reporting prevents false confidence.
  - Strongly typed schemas validated by Pydantic.
- **Negative / Trade-offs**:
  - Writing manifests requires upfront boilerplate for capability schema names and descriptions.
