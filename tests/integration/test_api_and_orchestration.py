"""Integration tests for FastAPI endpoints, orchestration, observability, and feedback."""

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_and_readiness_endpoints(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["data_mode"] == "synthetic"
    assert "provider" in data

    res = client.get("/api/v1/readiness")
    assert res.status_code == 200
    assert res.json()["ready"] is True
    assert res.json()["registered_agents_count"] == 10


def test_dashboard_summary_endpoint(client):
    res = client.get("/api/v1/dashboard/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["data_mode"] == "synthetic"
    assert "ethical_sales" in data
    assert "billing" in data
    assert "finance" in data
    assert "procurement" in data
    assert "logistics" in data
    assert "hr" in data


def test_agents_catalog_endpoints(client):
    res = client.get("/api/v1/agents")
    assert res.status_code == 200
    agents = res.json()
    assert len(agents) == 10

    res_single = client.get("/api/v1/agents/ethical_sales")
    assert res_single.status_code == 200
    assert res_single.json()["agent_id"] == "ethical_sales"

    res_404 = client.get("/api/v1/agents/non_existent_agent")
    assert res_404.status_code == 404


def test_integrations_status_endpoint(client):
    res = client.get("/api/v1/integrations/status")
    assert res.status_code == 200
    integrations = res.json()
    assert len(integrations) == 5
    system_ids = {i["system_id"] for i in integrations}
    assert "marg_erp" in system_ids
    assert "ordering_portal" in system_ids
    assert "whatsapp_ingest" in system_ids
    assert all(i["is_mock"] is True for i in integrations)


def test_ceo_chat_end_to_end_routing(client):
    # Query 1: Sales
    res1 = client.post("/api/v1/ceo/chat", json={"query": "How is Kolkata HQ sales performing?"})
    assert res1.status_code == 200
    d1 = res1.json()
    assert "ethical_sales" in d1["agents_invoked"]
    assert len(d1["evidence"]) > 0
    assert d1["data_mode"] == "synthetic"

    # Query 2: Inventory
    res2 = client.post("/api/v1/ceo/chat", json={"query": "Which stock is low and needs procurement reorder?"})
    assert res2.status_code == 200
    d2 = res2.json()
    assert "procurement" in d2["agents_invoked"]

    # Query 3: Finance
    res3 = client.post("/api/v1/ceo/chat", json={"query": "Give me overdue debtor accounts and aging"})
    assert res3.status_code == 200
    d3 = res3.json()
    assert "finance" in d3["agents_invoked"]


def test_ceo_daily_briefing_endpoint(client):
    res = client.get("/api/v1/ceo/daily-briefing")
    assert res.status_code == 200
    data = res.json()
    assert len(data["agents_invoked"]) >= 4
    assert "ethical_sales" in data["agents_invoked"]
    assert "procurement" in data["agents_invoked"]
    assert "finance" in data["agents_invoked"]
    assert "logistics" in data["agents_invoked"]


def test_observability_and_executions(client):
    # Trigger a chat to ensure an execution is saved
    chat_res = client.post("/api/v1/ceo/chat", json={"query": "Show dispatches and logistics delays"})
    exec_id = chat_res.json()["execution_id"]

    # Retrieve execution history
    res = client.get("/api/v1/executions")
    assert res.status_code == 200
    execs = res.json()
    assert len(execs) > 0
    assert any(e["execution_id"] == exec_id for e in execs)

    # Retrieve metrics
    met_res = client.get("/api/v1/observability/metrics")
    assert met_res.status_code == 200
    metrics = met_res.json()
    assert metrics["total_requests"] > 0
    assert "logistics" in metrics["agent_invocation_counts"]


def test_feedback_and_improvement_proposals(client):
    # Submit feedback
    fb_res = client.post(
        "/api/v1/feedback",
        json={
            "execution_id": "exec-test-99",
            "rating": "helpful",
            "comment": "Accurately surfaced delayed shipment LR number.",
            "reviewer_id": "lead-reviewer",
        },
    )
    assert fb_res.status_code == 200
    assert fb_res.json()["rating"] == "helpful"

    # List proposals
    prop_res = client.get("/api/v1/improvement-proposals")
    assert prop_res.status_code == 200
    pdata = prop_res.json()
    assert "proposals" in pdata
    assert len(pdata["proposals"]) >= 2
    assert "failure_analysis" in pdata


def test_simulated_approvals_queue(client):
    res = client.get("/api/v1/approvals")
    assert res.status_code == 200
    approvals = res.json()
    assert len(approvals) >= 2
    assert all(a["is_simulation"] is True for a in approvals)

    # Action on simulated approval
    act_res = client.post(f"/api/v1/approvals/{approvals[0]['id']}/action?action=approve")
    assert act_res.status_code == 200
    assert act_res.json()["is_simulation"] is True
