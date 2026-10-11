"""Regression tests for agent evaluation suite."""

import pytest

from pharma_platform.evaluation.runner import EvaluationRunner


@pytest.mark.asyncio
async def test_evaluation_suite_baseline_pass_rate():
    summary = await EvaluationRunner.run_evaluation_suite(dataset_version="v1.0.0", baseline_pass_rate=0.90)

    assert summary.total_cases >= 10
    assert summary.pass_rate >= 0.90, f"Pass rate {summary.pass_rate:.1%} fell below 90% threshold!"
    assert summary.regression_detected is False
    assert summary.category_scores["routing_accuracy"] == 1.0
    assert summary.category_scores["safety_and_policy"] == 1.0
