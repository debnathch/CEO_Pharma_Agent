# Agent Evaluation Framework & Quality Measurement

## 1. Evaluation Philosophy

In enterprise pharmaceutical systems, evaluations must be **deterministic, reproducible, and decoupled from the system under test**. We avoid self-judging models ("LLM-as-a-judge") for core business logic, schema contracts, and financial arithmetic.

---

## 2. Nine Evaluation Categories

The framework implements deterministic test cases across 9 essential dimensions:

1. **Routing Accuracy**: Did the CEO orchestrator route the request to the correct specialist agent?
2. **Contract Validity**: Does the returned payload conform to `AgentResult` schema with structured data?
3. **Data Correctness**: Are returned numbers identical to verified accounting and inventory calculations?
4. **Evidence Coverage**: Are all claims linked to authoritative source records (e.g. Marg ERP ledger)?
5. **Groundedness**: Does the response strictly avoid unsupported medical or financial hallucinations?
6. **Task Completion**: Did the workflow successfully answer the user inquiry?
7. **Safety & Policy Compliance**: Are unauthorized writes (purchase orders, disbursements) rejected? Are regulatory disclaimers attached?
8. **Robustness**: Does the platform handle unmapped HQs, empty strings, and missing entities without crashing?
9. **Latency & Resource Use**: Are execution durations within bounded operational budgets?

---

## 3. Dataset Specification (`v1.0.0`)

The dataset contains 12 comprehensive test cases:
- `EVAL-ROUTE-01`: Ethical Sales routing (Kolkata HQ).
- `EVAL-ROUTE-02`: Procurement low-stock routing (Amoxicillin).
- `EVAL-ROUTE-03`: Finance debtor aging routing.
- `EVAL-CONTRACT-01`: PCD Sales schema validation.
- `EVAL-DATA-01`: Deterministic billing gross margin verification (exact 28.8% margin).
- `EVAL-DATA-02`: Debtor >90d overdue risk detection (City Life Hospital).
- `EVAL-EVID-01`: Logistics consignment delay citation (Siliguri bypass).
- `EVAL-GROUND-01`: CEO morning briefing cross-domain grounding.
- `EVAL-TASK-01`: HR employee milestone detection (birthdays and anniversaries).
- `EVAL-SAFE-01`: Regulatory disclaimer enforcement on LBL draft.
- `EVAL-SAFE-02`: Verification that external marketing publishing is disabled.
- `EVAL-ROBUST-01`: Graceful handling of unmapped queries (Antarctica HQ).

---

## 4. Running Evaluations

### Via Command Line / Pytest
```bash
pytest tests/evaluation/
```

### Programmatic Python Invocation
```python
import asyncio
from pharma_platform.evaluation.runner import EvaluationRunner

async def main():
    summary = await EvaluationRunner.run_evaluation_suite(dataset_version="v1.0.0")
    print(f"Pass Rate: {summary.pass_rate * 100:.1f}%")
    print(f"Regression Detected: {summary.regression_detected}")

asyncio.run(main())
```

### Via REST API
```bash
curl -X POST "http://localhost:8000/api/v1/evaluations/run?dataset_version=v1.0.0"
```

### Via Command Center UI
Navigate to **Agent Evaluation** in the sidebar and click **Execute Evaluation Suite**. The UI displays the live pass rate gauge, category breakdown, and failure reasons.
