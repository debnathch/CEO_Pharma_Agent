import React, { useEffect, useState } from "react";
import { ShieldCheck, Check, X, AlertTriangle } from "lucide-react";
import { actionApproval, fetchApprovals } from "../services/api.ts";
import { ApprovalItem } from "../types.ts";

export const ApprovalsPage: React.FC = () => {
  const [approvals, setApprovals] = useState<ApprovalItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  useEffect(() => {
    fetchApprovals()
      .then(setApprovals)
      .finally(() => setLoading(false));
  }, []);

  const handleAction = async (id: string, action: string) => {
    try {
      const res = await actionApproval(id, action);
      setActionMessage(res.message);
      setApprovals((prev) =>
        prev.map((item) =>
          item.id === id ? { ...item, status: action === "approve" ? "simulated_approved" : "simulated_rejected" } : item
        )
      );
    } catch (err: any) {
      alert(`Action error: ${err.message}`);
    }
  };

  if (loading) {
    return <div style={{ padding: "40px", color: "#94a3b8" }}>Loading approvals queue...</div>;
  }

  return (
    <div>
      {/* Simulation Banner */}
      <div
        style={{
          backgroundColor: "#451a03",
          border: "1px solid #b45309",
          borderRadius: "8px",
          padding: "16px 20px",
          marginBottom: "24px",
          display: "flex",
          alignItems: "center",
          gap: "14px",
        }}
      >
        <AlertTriangle size={24} color="#fde68a" />
        <div style={{ fontSize: "0.875rem", color: "#fef3c7" }}>
          <strong>DEMONSTRATION SIMULATION QUEUE:</strong> The foundation phase strictly isolates write operations. No real purchase orders are submitted to manufacturers, and no financial banking disbursements occur. Natural language instructions cannot bypass approval policy boundaries.
        </div>
      </div>

      {actionMessage && (
        <div style={{ backgroundColor: "#064e3b", border: "1px solid #059669", padding: "12px 16px", borderRadius: "8px", marginBottom: "20px", color: "#a7f3d0", fontSize: "0.85rem" }}>
          {actionMessage}
        </div>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        {approvals.map((item) => (
          <div key={item.id} className="card">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
              <div>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "#f8fafc", marginBottom: "4px" }}>{item.title}</h3>
                <div style={{ fontSize: "0.8rem", color: "#64748b" }}>
                  ID: <code>{item.id}</code> • Requester: <strong>{item.requester}</strong> • Supplier: <strong>{item.supplier}</strong>
                </div>
              </div>
              <span className={`badge ${item.status.includes("approved") ? "badge-status-online" : item.status.includes("rejected") ? "badge-status-danger" : "badge-status-warning"}`}>
                {item.status.replace("_", " ").toUpperCase()}
              </span>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px", backgroundColor: "#0f172a", padding: "12px", borderRadius: "6px", fontSize: "0.85rem", marginBottom: "14px" }}>
              <div>
                <span style={{ color: "#64748b" }}>Estimated Cost:</span> <strong>{item.estimated_cost}</strong>
              </div>
              <div>
                <span style={{ color: "#64748b" }}>Requested At:</span> <span>{new Date(item.requested_at).toLocaleString()}</span>
              </div>
            </div>

            {item.status === "pending_executive_approval" && (
              <div style={{ display: "flex", gap: "10px", justifyContent: "flex-end", borderTop: "1px solid #334155", paddingTop: "12px" }}>
                <button
                  onClick={() => handleAction(item.id, "approve")}
                  className="btn-primary"
                  style={{ display: "flex", alignItems: "center", gap: "6px", backgroundColor: "#059669" }}
                >
                  <Check size={14} />
                  <span>Simulate Approve</span>
                </button>
                <button
                  onClick={() => handleAction(item.id, "reject")}
                  style={{ display: "flex", alignItems: "center", gap: "6px", backgroundColor: "#dc2626", color: "#fff", border: "none", borderRadius: "8px", padding: "12px 20px", fontWeight: 600, cursor: "pointer" }}
                >
                  <X size={14} />
                  <span>Simulate Reject</span>
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
