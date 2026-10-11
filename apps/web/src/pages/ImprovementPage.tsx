import React, { useEffect, useState } from "react";
import { GitBranch, Check, X, ShieldAlert, Sparkles, MessageSquare } from "lucide-react";
import { fetchProposals, reviewProposal } from "../services/api.ts";
import { ImprovementProposal } from "../types.ts";

export const ImprovementPage: React.FC = () => {
  const [proposals, setProposals] = useState<ImprovementProposal[]>([]);
  const [failureAnalysis, setFailureAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [reviewingId, setReviewingId] = useState<string | null>(null);
  const [reviewComment, setReviewComment] = useState("");

  const loadData = () => {
    setLoading(true);
    fetchProposals()
      .then((data) => {
        setProposals(data.proposals);
        setFailureAnalysis(data.failure_analysis);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleReview = async (proposalId: string, decision: "approved" | "rejected") => {
    try {
      await reviewProposal(proposalId, decision, reviewComment || "Reviewed via Executive UI");
      setReviewingId(null);
      setReviewComment("");
      loadData();
    } catch (err: any) {
      alert(`Review failed: ${err.message}`);
    }
  };

  if (loading && proposals.length === 0) {
    return <div style={{ padding: "40px", color: "#94a3b8" }}>Loading continuous improvement proposals...</div>;
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "approved":
        return <span className="badge badge-status-online">APPROVED (READY FOR RELEASE)</span>;
      case "released":
        return <span className="badge badge-provider">RELEASED</span>;
      case "rejected":
        return <span className="badge badge-status-danger">REJECTED</span>;
      default:
        return <span className="badge badge-status-warning">UNDER REVIEW</span>;
    }
  };

  return (
    <div>
      {/* Governance Notice */}
      <div
        style={{
          backgroundColor: "#1e1b4b",
          border: "1px solid #4338ca",
          borderRadius: "8px",
          padding: "14px 18px",
          marginBottom: "24px",
          display: "flex",
          alignItems: "center",
          gap: "12px",
        }}
      >
        <ShieldAlert size={20} color="#a5b4fc" />
        <div style={{ fontSize: "0.85rem", color: "#e0e7ff" }}>
          <strong>Controlled Improvement Governance:</strong> Agents do not autonomously modify their code or deploy unreviewed prompts. All improvements require structured failure diagnosis, proposal formulation, human review approval, and passing regression test suites prior to release.
        </div>
      </div>

      {/* Failure Analysis Diagnostics Summary */}
      {failureAnalysis && (
        <div className="card" style={{ marginBottom: "24px" }}>
          <h3 style={{ fontSize: "1.05rem", fontWeight: 700, marginBottom: "12px" }}>Automated Failure Mode Diagnosis</h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "16px" }}>
            <div style={{ backgroundColor: "#0f172a", padding: "14px", borderRadius: "8px" }}>
              <span style={{ fontSize: "0.75rem", color: "#64748b" }}>TOTAL EXECUTIONS ANALYZED</span>
              <div style={{ fontSize: "1.5rem", fontWeight: 700, marginTop: "4px" }}>{failureAnalysis.total_failures_analyzed}</div>
            </div>
            <div style={{ backgroundColor: "#0f172a", padding: "14px", borderRadius: "8px" }}>
              <span style={{ fontSize: "0.75rem", color: "#64748b" }}>NEGATIVE FEEDBACK SIGNALS</span>
              <div style={{ fontSize: "1.5rem", fontWeight: 700, marginTop: "4px", color: "#fbbf24" }}>{failureAnalysis.negative_feedback_count}</div>
            </div>
            <div style={{ backgroundColor: "#0f172a", padding: "14px", borderRadius: "8px" }}>
              <span style={{ fontSize: "0.75rem", color: "#64748b" }}>PRIMARY FAILURE CATEGORY</span>
              <div style={{ fontSize: "0.95rem", fontWeight: 700, marginTop: "8px", color: "#38bdf8" }}>
                {Object.keys(failureAnalysis.category_breakdown)[0] || "None Detected"}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Proposals List */}
      <div>
        <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "16px" }}>Improvement Proposals &amp; Release Review Gates</h3>
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          {proposals.map((prop) => (
            <div key={prop.proposal_id} className="card">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
                <div>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
                    <GitBranch size={18} color="#38bdf8" />
                    <h4 style={{ fontSize: "1.05rem", fontWeight: 700, color: "#f8fafc" }}>{prop.title}</h4>
                  </div>
                  <div style={{ fontSize: "0.8rem", color: "#64748b" }}>
                    ID: <code>{prop.proposal_id}</code> • Target Agent: <code>{prop.target_agent_id}</code> • Type: <strong>{prop.proposal_type}</strong>
                  </div>
                </div>
                {getStatusBadge(prop.status)}
              </div>

              <p style={{ fontSize: "0.9rem", color: "#cbd5e1", marginBottom: "12px" }}>{prop.description}</p>

              <div style={{ backgroundColor: "#0f172a", padding: "12px", borderRadius: "6px", fontSize: "0.85rem", marginBottom: "14px" }}>
                <strong style={{ color: "#94a3b8", display: "block", fontSize: "0.75rem", marginBottom: "4px" }}>RATIONALE &amp; EVIDENCE:</strong>
                <span style={{ color: "#e2e8f0" }}>{prop.rationale}</span>
              </div>

              {/* Review Actions */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderTop: "1px solid #334155", paddingTop: "12px" }}>
                <div style={{ fontSize: "0.8rem", color: "#64748b" }}>
                  Regression Suite: <strong style={{ color: prop.regression_suite_passed ? "#34d399" : "#fbbf24" }}>{prop.regression_suite_passed ? "Passed Baseline (Safe)" : "Pending Verification"}</strong>
                </div>

                {prop.status === "under_review" || prop.status === "draft" ? (
                  <div style={{ display: "flex", gap: "8px" }}>
                    <button
                      onClick={() => handleReview(prop.proposal_id, "approved")}
                      className="btn-primary"
                      style={{ display: "flex", alignItems: "center", gap: "4px", backgroundColor: "#059669", padding: "6px 14px", fontSize: "0.8rem" }}
                    >
                      <Check size={14} />
                      <span>Approve Proposal</span>
                    </button>
                    <button
                      onClick={() => handleReview(prop.proposal_id, "rejected")}
                      style={{ display: "flex", alignItems: "center", gap: "4px", backgroundColor: "#dc2626", color: "#fff", border: "none", borderRadius: "6px", padding: "6px 14px", fontSize: "0.8rem", cursor: "pointer" }}
                    >
                      <X size={14} />
                      <span>Reject</span>
                    </button>
                  </div>
                ) : (
                  <div style={{ fontSize: "0.8rem", color: "#94a3b8" }}>
                    Reviewed by: <strong>{prop.reviewed_by || "Reviewer"}</strong> ({prop.review_comments || "No comments"})
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
