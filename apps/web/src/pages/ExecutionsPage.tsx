import React, { useEffect, useState } from "react";
import { History, Eye, X } from "lucide-react";
import { fetchExecutions } from "../services/api.ts";
import { ExecutionRecord } from "../types.ts";

export const ExecutionsPage: React.FC = () => {
  const [executions, setExecutions] = useState<ExecutionRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedExec, setSelectedExec] = useState<ExecutionRecord | null>(null);

  useEffect(() => {
    fetchExecutions()
      .then(setExecutions)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div style={{ padding: "40px", color: "#94a3b8" }}>Loading execution history...</div>;
  }

  return (
    <div>
      <div style={{ marginBottom: "20px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <p style={{ color: "#94a3b8", fontSize: "0.95rem" }}>
          Persisted execution records from the CEO bounded orchestration engine. Traceable via unique correlation IDs.
        </p>
        <span className="badge badge-provider">{executions.length} EXECUTIONS RECORDED</span>
      </div>

      {executions.length === 0 ? (
        <div className="card" style={{ textAlign: "center", padding: "48px 24px" }}>
          <History size={36} color="#64748b" style={{ margin: "0 auto 12px" }} />
          <h3 style={{ fontSize: "1.1rem", marginBottom: "8px" }}>No Execution Records Yet</h3>
          <p style={{ color: "#94a3b8", fontSize: "0.85rem" }}>
            Submit an inquiry through the CEO Chat or run an evaluation suite to populate execution records.
          </p>
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Execution ID</th>
                <th>Correlation ID</th>
                <th>User Query</th>
                <th>Status</th>
                <th>Agents Invoked</th>
                <th>Latency</th>
                <th>Provider</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {executions.map((ex) => (
                <tr key={ex.execution_id}>
                  <td>
                    <code>{ex.execution_id}</code>
                  </td>
                  <td>
                    <span style={{ fontSize: "0.75rem", color: "#94a3b8" }}>{ex.correlation_id.substring(0, 8)}...</span>
                  </td>
                  <td style={{ maxWidth: "260px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                    {ex.user_query}
                  </td>
                  <td>
                    <span
                      className={`badge ${
                        ex.status === "success"
                          ? "badge-status-online"
                          : ex.status === "partial"
                          ? "badge-status-warning"
                          : "badge-status-danger"
                      }`}
                    >
                      {ex.status.toUpperCase()}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: "flex", gap: "4px", flexWrap: "wrap" }}>
                      {(ex.agents_invoked || []).map((a) => (
                        <span key={a} style={{ fontSize: "0.7rem", backgroundColor: "#0f172a", padding: "2px 6px", borderRadius: "4px", color: "#38bdf8" }}>
                          {a}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td>{ex.duration_ms}ms</td>
                  <td>
                    <span className="badge badge-provider">{ex.provider_mode}</span>
                  </td>
                  <td>
                    <button
                      onClick={() => setSelectedExec(ex)}
                      style={{ background: "none", border: "none", color: "#38bdf8", cursor: "pointer", display: "flex", alignItems: "center", gap: "4px" }}
                    >
                      <Eye size={14} />
                      <span>Details</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Details Modal / Drawer */}
      {selectedExec && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0,0,0,0.7)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 9999,
          }}
        >
          <div
            style={{
              backgroundColor: "#1e293b",
              border: "1px solid #334155",
              borderRadius: "12px",
              width: "90%",
              maxWidth: "700px",
              maxHeight: "85vh",
              overflowY: "auto",
              padding: "24px",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <h3 style={{ fontSize: "1.1rem", fontWeight: 700 }}>Execution Details: <code>{selectedExec.execution_id}</code></h3>
              <button onClick={() => setSelectedExec(null)} style={{ background: "none", border: "none", color: "#94a3b8", cursor: "pointer" }}>
                <X size={20} />
              </button>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "12px", fontSize: "0.85rem" }}>
              <div>
                <strong style={{ color: "#64748b" }}>Query:</strong>
                <div style={{ marginTop: "4px", padding: "8px", backgroundColor: "#0f172a", borderRadius: "6px" }}>{selectedExec.user_query}</div>
              </div>

              <div>
                <strong style={{ color: "#64748b" }}>Summary:</strong>
                <div style={{ marginTop: "4px", padding: "8px", backgroundColor: "#0f172a", borderRadius: "6px", whiteSpace: "pre-line" }}>{selectedExec.summary}</div>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
                <div>
                  <strong style={{ color: "#64748b" }}>Status:</strong> {selectedExec.status}
                </div>
                <div>
                  <strong style={{ color: "#64748b" }}>Duration:</strong> {selectedExec.duration_ms} ms
                </div>
                <div>
                  <strong style={{ color: "#64748b" }}>Provider Mode:</strong> {selectedExec.provider_mode}
                </div>
                <div>
                  <strong style={{ color: "#64748b" }}>Evidence Records:</strong> {selectedExec.evidence_count}
                </div>
              </div>

              {selectedExec.warnings && selectedExec.warnings.length > 0 && (
                <div>
                  <strong style={{ color: "#fbbf24" }}>Warnings:</strong>
                  <div style={{ marginTop: "4px", padding: "8px", backgroundColor: "#451a03", borderRadius: "6px", color: "#fef3c7" }}>
                    {selectedExec.warnings.map((w, idx) => (
                      <div key={idx}>• {w}</div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
