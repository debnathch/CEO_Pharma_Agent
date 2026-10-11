import React, { useEffect, useState } from "react";
import { Database, Globe, MessageSquare, Share2, Users, ShieldAlert, CheckCircle } from "lucide-react";
import { fetchIntegrations } from "../services/api.ts";
import { IntegrationHealth } from "../types.ts";

export const IntegrationsPage: React.FC = () => {
  const [integrations, setIntegrations] = useState<IntegrationHealth[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchIntegrations()
      .then(setIntegrations)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div style={{ padding: "40px", color: "#94a3b8" }}>Loading integration adapter statuses...</div>;
  }

  const getIcon = (id: string) => {
    switch (id) {
      case "marg_erp":
        return <Database size={22} color="#38bdf8" />;
      case "ordering_portal":
        return <Globe size={22} color="#818cf8" />;
      case "whatsapp_ingest":
        return <MessageSquare size={22} color="#34d399" />;
      case "social_media":
        return <Share2 size={22} color="#f472b6" />;
      case "hr_records":
        return <Users size={22} color="#fbbf24" />;
      default:
        return <Database size={22} />;
    }
  };

  return (
    <div>
      {/* Notice Banner */}
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
          <strong>Explicit Boundary &amp; Ownership Rules:</strong> All integrations run in isolated synthetic mock adapters. Live ordering portal (<code>http://bengalremedies.com:9000</code>) and internal Marg ERP are decoupled to protect production records. WhatsApp content is non-authoritative evidence.
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(360px, 1fr))", gap: "20px" }}>
        {integrations.map((item) => (
          <div key={item.system_id} className="card">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <div style={{ padding: "8px", backgroundColor: "#0f172a", borderRadius: "8px" }}>{getIcon(item.system_id)}</div>
                <div>
                  <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "#f8fafc" }}>{item.display_name}</h3>
                  <div style={{ fontSize: "0.8rem", color: "#64748b" }}>ID: <code>{item.system_id}</code></div>
                </div>
              </div>
              <span className="badge badge-status-online">
                <CheckCircle size={12} />
                CONNECTED
              </span>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "10px", fontSize: "0.85rem" }}>
              <div style={{ backgroundColor: "#0f172a", padding: "10px", borderRadius: "6px" }}>
                <span style={{ color: "#64748b", display: "block", fontSize: "0.75rem", marginBottom: "4px" }}>
                  SYSTEM AUTHORITY SCOPE:
                </span>
                <span style={{ color: "#cbd5e1" }}>{item.authority_scope}</span>
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", color: "#94a3b8", fontSize: "0.8rem" }}>
                <span>Adapter Type:</span>
                <span style={{ color: "#38bdf8", fontWeight: 600 }}>Synthetic Mock (Zero Risk)</span>
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", color: "#94a3b8", fontSize: "0.8rem" }}>
                <span>Status:</span>
                <span>{item.status_message}</span>
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", color: "#64748b", fontSize: "0.75rem", borderTop: "1px solid #334155", paddingTop: "8px" }}>
                <span>Last Sync:</span>
                <span>{new Date(item.last_sync_timestamp).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
