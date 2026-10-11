"""Evaluation Runner and Regression Suite Engine."""

import uuid
from collections import defaultdict
from datetime import datetime, timezone

from pharma_platform.contracts.evaluation import (
    EvaluationResult,
    EvaluationRunSummary,
)
from pharma_platform.evaluation.dataset import get_dataset
from pharma_platform.evaluation.evaluators import DeterministicEvaluator
from pharma_platform.orchestration.workflow import run_ceo_workflow
from pharma_platform.persistence.database import get_session
from pharma_platform.persistence.models import EvaluationRunModel
from pharma_platform.providers.factory import get_llm_provider


class EvaluationRunner:
    """Executes evaluation test suites against the active platform configuration."""

    @staticmethod
    async def run_evaluation_suite(
        dataset_version: str = "v1.0.0",
        baseline_pass_rate: float = 0.90,
    ) -> EvaluationRunSummary:
        start_time = datetime.now(timezone.utc)
        run_id = f"eval-run-{str(uuid.uuid4())[:8]}"
        dataset = get_dataset(dataset_version)
        provider = get_llm_provider()

        results: list[EvaluationResult] = []
        category_totals: dict[str, int] = defaultdict(int)
        category_passes: dict[str, int] = defaultdict(int)

        for case in dataset:
            # Run query through the CEO orchestration workflow
            exec_state = await run_ceo_workflow(
                user_query=case.user_query,
                context={"user_role": "EvaluationRunner", "user_id": "eval-bot"},
            )

            result = DeterministicEvaluator.evaluate_case(
                case=case,
                run_id=run_id,
                execution_state=exec_state,
            )
            results.append(result)

            cat_key = case.category.value
            category_totals[cat_key] += 1
            if result.passed:
                category_passes[cat_key] += 1

        end_time = datetime.now(timezone.utc)
        total_cases = len(results)
        passed_cases = sum(1 for r in results if r.passed)
        failed_cases = total_cases - passed_cases
        pass_rate = round(passed_cases / total_cases, 4) if total_cases > 0 else 0.0

        category_scores = {}
        for cat, total in category_totals.items():
            category_scores[cat] = round(category_passes[cat] / total, 2) if total > 0 else 0.0

        regression_detected = pass_rate < baseline_pass_rate
        regression_details = []
        if regression_detected:
            regression_details.append(
                f"Pass rate {pass_rate:.1%} fell below minimum baseline threshold {baseline_pass_rate:.1%}!"
            )

        summary = EvaluationRunSummary(
            run_id=run_id,
            dataset_version=dataset_version,
            model_mode=provider.provider_name,
            model_identifier=getattr(provider, "_model_name", "default"),
            start_time=start_time,
            end_time=end_time,
            total_cases=total_cases,
            passed_cases=passed_cases,
            failed_cases=failed_cases,
            pass_rate=pass_rate,
            category_scores=category_scores,
            results=results,
            regression_detected=regression_detected,
            regression_details=regression_details,
        )

        # Persist run in DB
        try:
            session = get_session()
            db_run = EvaluationRunModel(
                run_id=run_id,
                dataset_version=dataset_version,
                model_mode=summary.model_mode,
                model_identifier=summary.model_identifier,
                total_cases=total_cases,
                passed_cases=passed_cases,
                failed_cases=failed_cases,
                pass_rate=pass_rate,
                category_scores=category_scores,
                results_json=[r.model_dump(mode="json") for r in results],
                regression_detected=regression_detected,
            )
            session.add(db_run)
            session.commit()
            session.close()
        except Exception:
            pass

        return summary
