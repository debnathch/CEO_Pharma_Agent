# ADR-005: Separation of Deterministic Domain Calculations from LLM Reasoning

## Status
Accepted

## Context
Large Language Models are probabilistic token predictors and are fundamentally unsuited for authoritative financial accounting, ledger reconciliation, gross profit margin percentages, and safety inventory threshold calculations. Delegating arithmetic to an LLM introduces hallucinated figures, rounding errors, and un-auditable outputs that are unacceptable in enterprise pharmaceutical governance.

## Decision
All business mathematics, accounting aggregations, gross margin computations, debtor aging classification, and safety stock reorder thresholds are implemented as **deterministic Python business services** (`src/pharma_platform/business_services/*`).
- `SalesService`: MTD targets, achievements, and percentages.
- `BillingService`: Exact formula: `Gross Profit = Net Sales - (COGS + Free Goods Cost)`.
- `FinanceService`: Strict aging day buckets (0-30, 31-60, 61-90, >90).
- `ProcurementService`: Strict threshold comparison: `Stock <= Reorder Threshold`.
The LLM is strictly used as an executive summarizer and conversational narrator over verified numbers; it is never permitted to calculate or invent financial values.

## Alternatives Considered
1. **Prompting the LLM to calculate margins**:
   - *Rejected*: Prone to mathematical errors and non-reproducible calculations.
2. **LLM Code Interpreter tool**:
   - *Rejected*: Adds runtime complexity and security sandboxing risks for simple deterministic business rules.

## Consequences & Trade-offs
- **Positive**:
  - 100% reproducible and unit-testable accounting calculations.
  - Transparent audit trail with exact costing formulas.
- **Negative / Trade-offs**:
  - New calculations require adding or extending Python services rather than adjusting prompts.
