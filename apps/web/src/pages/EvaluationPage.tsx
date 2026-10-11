import React, { useEffect, useState } from "react";
import { CheckCircle2, XCircle, Play, ShieldCheck, AlertOctagon, RefreshCw } from "lucide-react";
import { fetchEvaluations, runEvaluationSuite } from "../services/api.ts";
import { EvaluationRun } from "../types.ts";

export const EvaluationPage: React.FC = () => {
  const [runs, setRuns] = useState<EvaluationRun[]>([]);
  const [selectedRun, setSelectedRun] = useState<EvaluationRun | null>(null);
  const [running, setRunning] = useState(false);
  const [loading, setLoading] = useState(true);

  const loadRuns = () => {
    setLoading(true);
    fetchEvaluations()
      .then((data) => {
        setRuns(data);
        if (data.length > 0 && !selectedRun) {
          setSelectedRun(data[0]);
        }
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadRuns();
  }, []);

  const handleRunSuite = async () => {
    setRunning(true);
    try {
      const summary = await runEvaluationSuite("v1.0.0");
      setRuns((prev) => [summary, ...prev]);
      setSelectedRun(summary);
    } catch (err: any) {
      alert(`Evaluation run failed: ${err.message}`);
    } finally {
      setRunning(false);
    }
  };

  if (loading && runs.length === 0) {
    return <div style={{ padding: "40px", color: "#94a3b8" }}>Loading evaluation test harness...</div>;
  }

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
        <div>
          <p style={{ color: "#94a3b8", fontSize: "0.95rem" }}>
            Automated quality measurement and regression suite. Evaluates routing, contracts, deterministic business data, and safety policy.
          </p>
        </div>
        <button
          className="btn-primary"
          onClick={handleRunSuite}
          disabled={running}
          style={{ display: "flex", alignItems: "center", gap: "8px" }}
        >
          {running ? <RefreshCw size={16} className="animate-spin" /> : <Play size={16} />}
          <span>{running ? "Running Evaluation Suite..." : "Execute Evaluation Suite"}</span>
        </button>
      </div>

      {runs.length === 0 ? (
        <div className="card" style={{ textAlign: "center", padding: "48px 24px" }}>
          <ShieldCheck size={36} color="#64748b" style={{ margin: "0 auto 12px" }} />
          <h3 style={{ fontSize: "1.1rem", marginBottom: "8px" }}>No Evaluation Runs Yet</h3>
          <p style={{ color: "#94a3b8", fontSize: "0.85rem", marginBottom: "16px" }}>
            Execute the synthetic evaluation suite to benchmark the current platform release.
          </p>
          <button className="btn-primary" onClick={handleRunSuite} disabled={running}>
            Run v1.0.0 Evaluation Suite
          </button>
        </div>
      ) : (
        <>
          {/* Active Run Header Cards */}
          {selectedRun && (
            <div className="grid-cards">
              <div className="card">
                <span className="card-title">Suite Pass Rate</span>
                <div className="card-value" style={{ color: selectedRun.pass_rate >= 0.9 ? "#34d399" : "#f87171" }}>
                  {(selectedRun.pass_rate * 100).toFixed(1)}%
                </div>
                <div className="card-subtitle">
                  {selectedRun.passed_cases} passed of {selectedRun.total_cases} test cases
                </div>
              </div>

              <div className="card">
                <span className="card-title">Regression Status</span>
                <div className="card-value" style={{ fontSize: "1.3rem", marginTop: "6px" }}>
                  {selectedRun.regression_detected ? (
                    <span style={{ color: "#f87171", display: "flex", alignItems: "center", gap: "6px" }}>
                      <AlertOctagon size={20} /> REGRESSION DETECTED
                    </span>
                  ) : (
                    <span style={{ color: "#34d399", display: "flex", alignItems: "center", gap: "6px" }}>
                      <CheckCircle2 size={20} /> STABLE BASELINE
                    </span>
                  )}
                </div>
                <div className="card-subtitle">Dataset Version: <strong>{selectedRun.dataset_version}</strong></div>
              </div>

              <div className="card">
                <span className="card-title">Inference Engine Tested</span>
                <div className="card-value" style={{ fontSize: "1.2rem", marginTop: "6px" }}>
                  <span className="badge badge-provider">{selectedRun.model_mode.toUpperCase()}</span>
                </div>
                <div className="card-subtitle">Model: {selectedRun.model_identifier}</div>
              </div>

              <div className="card">
                <span className="card-title">Run Identifier</span>
                <div className="card-value" style={{ fontSize: "1.1rem", marginTop: "6px" }}>
                  <code>{selectedRun.run_id}</code>
                </div>
                <div className="card-subtitle">
                  {selectedRun.created_at ? new Date(selectedRun.created_at).toLocaleString() : "Recent Run"}
                </div>
              </div>
            </div>
          )}

          {/* Category Scores */}
          {selectedRun && selectedRun.category_scores && (
            <div className="card" style={{ marginBottom: "24px" }}>
              <h3 style={{ fontSize: "1.05rem", fontWeight: 700, marginBottom: "16px" }}>Evaluation Category Scores</h3>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "12px" }}>
                {Object.entries(selectedRun.category_scores).map(([cat, score]) => (
                  <div key={cat} style={{ backgroundColor: "#0f172a", padding: "12px", borderRadius: "8px" }}>
                    <div style={{ fontSize: "0.75rem", color: "#94a3b8", textTransform: "capitalize", marginBottom: "4px" }}>
                      {cat.replace("_", " ")}
                    </div>
                    <div style={{ fontSize: "1.2rem", fontWeight: 700, color: score >= 0.9 ? "#34d399" : score >= 0.7 ? "#fbbf24" : "#f87171" }}>
                      {(score * 100).toFixed(0)}%
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recent Runs Table */}
          <div className="card">
            <h3 style={{ fontSize: "1.05rem", fontWeight: 700, marginBottom: "16px" }}>Historical Evaluation Runs</h3>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Run ID</th>
                    <th>Dataset</th>
                    <th>Model Mode</th>
                    <th>Pass Rate</th>
                    <th>Outcome</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {runs.map((r) => (
                    <tr key={r.run_id} style={{ backgroundColor: selectedRun?.run_id === r.run_id ? "rgba(2, 132, 199, 0.15)" : undefined }}>
                      <td><code>{r.run_id}</code></td>
                      <td>{r.dataset_version}</td>
                      <td><span className="badge badge-provider">{r.model_mode}</span></td>
                      <td style={{ fontWeight: 600, color: r.pass_rate >= 0.9 ? "#34d399" : "#f87171" }}>
                        {(r.pass_rate * 100).toFixed(1)}% ({r.passed_cases}/{r.total_cases})
                      </td>
                      <td>
                        {r.regression_detected ? (
                          <span className="badge badge-status-danger">REGRESSION</span>
                        ) : (
                          <span className="badge badge-status-online">PASSED</span>
                        )}
                      </td>
                      <td>
                        <button
                          onClick={() => setSelectedRun(r)}
                          style={{ background: "none", border: "none", color: "#38bdf8", cursor: "pointer", fontSize: "0.8rem" }}
                        >
                          View Breakdown
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
