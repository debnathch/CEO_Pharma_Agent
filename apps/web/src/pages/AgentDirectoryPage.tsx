import React, { useEffect, useState } from "react";
import { Cpu, CheckCircle2, AlertCircle, Shield, Wrench } from "lucide-react";
import { fetchAgents } from "../services/api.ts";
import { AgentManifest } from "../types.ts";

export const AgentDirectoryPage: React.FC = () => {
  const [agents, setAgents] = useState<AgentManifest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAgents()
      .then(setAgents)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div style={{ padding: "40px", color: "#94a3b8" }}>Loading agent registry catalog...</div>;
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "full":
        return <span className="badge badge-status-online">FULL IMPLEMENTATION</span>;
      case "partial":
        return <span className="badge badge-provider">FOUNDATION ACTIVE</span>;
      default:
        return <span className="badge badge-status-warning">SKELETON CONTRACT</span>;
    }
  };

  return (
    <div>
      <div style={{ marginBottom: "24px" }}>
        <p style={{ color: "#94a3b8", fontSize: "0.95rem" }}>
          Registered specialist agents in the ecosystem. Every agent conforms to the standardized <code>AgentManifest</code> contract and reports honest capability readiness.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(420px, 1fr))", gap: "20px" }}>
        {agents.map((agent) => (
          <div key={agent.agent_id} className="card" style={{ display: "flex", flexDirection: "column" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
                  <Cpu size={18} color="#38bdf8" />
                  <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "#f8fafc" }}>{agent.display_name}</h3>
                </div>
                <div style={{ fontSize: "0.8rem", color: "#64748b" }}>
                  ID: <code>{agent.agent_id}</code> • Domain: <strong>{agent.domain}</strong> • v{agent.version}
                </div>
              </div>
              {getStatusBadge(agent.implementation_status)}
            </div>

            <p style={{ fontSize: "0.85rem", color: "#94a3b8", marginBottom: "16px", flex: 1 }}>{agent.description}</p>

            {/* Declared Capabilities */}
            <div style={{ backgroundColor: "#0f172a", borderRadius: "8px", padding: "12px", marginBottom: "14px" }}>
              <div style={{ fontSize: "0.75rem", textTransform: "uppercase", fontWeight: 600, color: "#64748b", marginBottom: "8px" }}>
                Declared Capabilities ({agent.capabilities.length})
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                {agent.capabilities.map((cap) => (
                  <div key={cap.name} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", fontSize: "0.8rem" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                      {cap.is_implemented ? (
                        <CheckCircle2 size={14} color="#34d399" />
                      ) : (
                        <AlertCircle size={14} color="#fbbf24" />
                      )}
                      <span style={{ color: cap.is_implemented ? "#f1f5f9" : "#94a3b8" }}>{cap.name}</span>
                    </div>
                    <span style={{ fontSize: "0.7rem", color: cap.is_implemented ? "#34d399" : "#fbbf24" }}>
                      {cap.is_implemented ? "Active" : "Planned (Phase 2)"}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Permissions & Tools */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: "0.75rem", color: "#64748b", borderTop: "1px solid #334155", paddingTop: "12px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
                <Shield size={14} />
                <span>Perms: {agent.required_permissions.join(", ") || "None"}</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
                <Wrench size={14} />
                <span>Tools: {agent.supported_tools.join(", ") || "None"}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
