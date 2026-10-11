import React, { useEffect, useState } from "react";
import { Activity, Zap, CheckCircle2, AlertTriangle, XCircle, RefreshCw } from "lucide-react";
import { fetchMetrics } from "../services/api.ts";
import { MetricSummary } from "../types.ts";

export const ObservabilityPage: React.FC = () => {
  const [metrics, setMetrics] = useState<MetricSummary | null>(null);
  const [loading, setLoading] = useState(true);

  const loadData = () => {
    setLoading(true);
    fetchMetrics()
      .then(setMetrics)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading && !metrics) {
    return <div style={{ padding: "40px", color: "#94a3b8" }}>Loading observability telemetry...</div>;
  }

  if (!metrics) {
    return <div style={{ padding: "40px", color: "#f87171" }}>Failed to load metrics.</div>;
  }

  const successRate = metrics.total_requests > 0
    ? ((metrics.successful_executions / metrics.total_requests) * 100).toFixed(1)
    : "100.0";

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
        <p style={{ color: "#94a3b8", fontSize: "0.95rem" }}>
          Platform observability and performance telemetry. All metrics reflect real execution traces.
        </p>
        <button className="btn-primary" onClick={loadData} style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "0.85rem", padding: "8px 16px" }}>
          <RefreshCw size={14} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Metric KPI Cards */}
      <div className="grid-cards">
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <span className="card-title">Total Requests</span>
            <Activity size={20} color="#38bdf8" />
          </div>
          <div className="card-value">{metrics.total_requests}</div>
          <div className="card-subtitle">All orchestrator &amp; agent executions</div>
        </div>

        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <span className="card-title">Execution Success Rate</span>
            <CheckCircle2 size={20} color="#34d399" />
          </div>
          <div className="card-value" style={{ color: "#34d399" }}>{successRate}%</div>
          <div className="card-subtitle">{metrics.successful_executions} successful, {metrics.partial_executions} partial</div>
        </div>

        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <span className="card-title">Latency (Avg / p95)</span>
            <Zap size={20} color="#fbbf24" />
          </div>
          <div className="card-value">{metrics.average_duration_ms}ms</div>
          <div className="card-subtitle">p95 Latency: <strong style={{ color: "#fbbf24" }}>{metrics.p95_duration_ms}ms</strong></div>
        </div>

        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <span className="card-title">LLM Provider Status</span>
            <span className="badge badge-provider">{metrics.provider_mode.toUpperCase()}</span>
          </div>
          <div className="card-value" style={{ fontSize: "1.25rem", marginTop: "8px", color: metrics.provider_available ? "#34d399" : "#f87171" }}>
            {metrics.provider_available ? "Online (Available)" : "Unavailable"}
          </div>
          <div className="card-subtitle">Zero API fee local inference / mock fallback</div>
        </div>
      </div>

      {/* Specialist Agent Invocation Telemetry */}
      <div className="card" style={{ marginBottom: "24px" }}>
        <h3 style={{ fontSize: "1.05rem", fontWeight: 700, marginBottom: "16px" }}>Specialist Agent Invocations &amp; Reliability</h3>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Agent Identifier</th>
                <th>Invocations Count</th>
                <th>Success Rate (%)</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(metrics.agent_invocation_counts).length === 0 ? (
                <tr>
                  <td colSpan={4} style={{ textAlign: "center", color: "#64748b" }}>No agent invocations recorded yet.</td>
                </tr>
              ) : (
                Object.entries(metrics.agent_invocation_counts).map(([agent, count]) => {
                  const rate = metrics.agent_success_rates[agent] ?? 100.0;
                  return (
                    <tr key={agent}>
                      <td><code>{agent}</code></td>
                      <td>{count}</td>
                      <td>
                        <span style={{ color: rate >= 90 ? "#34d399" : rate >= 70 ? "#fbbf24" : "#f87171", fontWeight: 600 }}>
                          {rate}%
                        </span>
                      </td>
                      <td>
                        <span className="badge badge-status-online">HEALTHY</span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
