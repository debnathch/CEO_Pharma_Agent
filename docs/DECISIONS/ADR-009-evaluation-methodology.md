# ADR-009: Agent Evaluation Methodology and Deterministic Regression Harness

## Status
Accepted

## Context
Many AI projects evaluate agents by having an LLM judge its own responses ("LLM-as-a-judge"), resulting in circular logic, high variance, and self-reinforcing errors. For pharmaceutical operations, evaluation must be reproducible, objective, and distinct from production execution.

## Decision
We implement an explicit **Evaluation Framework** (`src/pharma_platform/evaluation/*`):
1. **Version-Controlled Synthetic Evaluation Datasets**: Dataset `v1.0.0` with distinct test cases covering 9 explicit categories:
   - Routing Accuracy
   - Contract Validity
   - Data Correctness
   - Evidence Coverage
   - Groundedness
   - Task Completion
   - Safety & Policy Compliance
   - Robustness
   - Latency & Resource Use
2. **Deterministic Evaluator**: Verifies schema contracts, exact business figures, required keywords, and absence of prohibited claims using deterministic assertions.
3. **EvaluationRunner**: Executes test cases against the active platform, calculates category scores, compares against baseline thresholds (90%), and flags regressions.

## Alternatives Considered
1. **Relying solely on LLM self-evaluation**:
   - *Rejected*: Inconsistent, expensive, and cannot authoritatively verify arithmetic correctness.
2. **Manual ad-hoc chat prompt testing**:
   - *Rejected*: Cannot catch silent regressions introduced during agent refactoring or prompt adjustments.

## Consequences & Trade-offs
- **Positive**:
  - Deterministic test cases run reliably in CI and local test harnesses.
  - Regression detection halts unsafe deployments.
- **Negative / Trade-offs**:
  - Requires maintaining ground-truth test fixtures and updating expected keywords when underlying synthetic datasets expand.
