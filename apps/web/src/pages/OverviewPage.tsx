import React, { useEffect, useState } from "react";
import {
  TrendingUp,
  Package,
  FileText,
  AlertTriangle,
  Truck,
  Users,
  CheckCircle,
  Clock,
  Sparkles,
} from "lucide-react";
import { fetchDashboardSummary } from "../services/api.ts";
import { DashboardSummary } from "../types.ts";

export const OverviewPage: React.FC = () => {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardSummary()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div style={{ padding: "40px", color: "#94a3b8" }}>Loading executive business dashboard...</div>;
  }

  if (error || !data) {
    return <div style={{ padding: "40px", color: "#f87171" }}>Failed to load dashboard: {error}</div>;
  }

  return (
    <div>
      {/* Synthetic Banner */}
      <div
        style={{
          backgroundColor: "#1e1b4b",
          border: "1px solid #4338ca",
          borderRadius: "8px",
          padding: "12px 18px",
          marginBottom: "24px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <Sparkles size={18} color="#a5b4fc" />
          <span style={{ fontSize: "0.85rem", color: "#e0e7ff" }}>
            <strong>Executive Sandbox Environment:</strong> All records are verified synthetic data. Reporting snapshot date: <strong>{data.as_of_date}</strong>. Live systems remain uncalled.
          </span>
        </div>
        <span className="badge badge-synthetic">SYNTHETIC DATA</span>
      </div>

      {/* Grid of Business Domain Cards */}
      <div className="grid-cards">
        {/* Ethical Sales Card */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <span className="card-title">Ethical Sales (MTD)</span>
            <TrendingUp size={20} color="#38bdf8" />
          </div>
          <div className="card-value">₹{(data.ethical_sales.total_achieved_mtd / 100000).toFixed(2)}L</div>
          <div className="card-subtitle">
            Target: ₹{(data.ethical_sales.total_target_mtd / 100000).toFixed(2)}L (<strong>{data.ethical_sales.overall_achievement_pct}%</strong>)
          </div>
          <div style={{ marginTop: "12px", fontSize: "0.8rem", color: "#38bdf8" }}>
            Top HQ: <strong>{data.ethical_sales.top_performing_hq}</strong> (107.4%)
          </div>
        </div>

        {/* PCD Sales Card */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <span className="card-title">PCD Franchise Revenue</span>
            <Package size={20} color="#818cf8" />
          </div>
          <div className="card-value">₹{(data.pcd_sales.total_revenue / 100000).toFixed(2)}L</div>
          <div className="card-subtitle">Across {data.pcd_sales.distributor_count} authorized franchise distributors</div>
          <div style={{ marginTop: "12px", fontSize: "0.8rem", color: "#a5b4fc" }}>
            Pending pipeline: ₹{(data.pcd_sales.pending_orders / 1000).toFixed(0)}k
          </div>
        </div>

        {/* Billing & Margin Card */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <span className="card-title">Gross Profit & Margin</span>
            <FileText size={20} color="#34d399" />
          </div>
          <div className="card-value">{data.billing.overall_gross_margin_pct}%</div>
          <div className="card-subtitle">
            Gross Profit: ₹{data.billing.total_gross_profit.toLocaleString()} on ₹{data.billing.total_invoiced_net.toLocaleString()} net
          </div>
          {data.billing.low_margin_alerts_count > 0 && (
            <div style={{ marginTop: "12px", fontSize: "0.8rem", color: "#fbbf24", display: "flex", alignItems: "center", gap: "6px" }}>
              <AlertTriangle size={14} />
              <span>{data.billing.low_margin_alerts_count} invoice(s) with margin &lt;15%</span>
            </div>
          )}
        </div>

        {/* Debtors & Credit Risk Card */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <span className="card-title">Outstanding Debtors</span>
            <AlertTriangle size={20} color="#f87171" />
          </div>
          <div className="card-value">₹{(data.finance.total_debtors_outstanding / 1000).toFixed(0)}k</div>
          <div className="card-subtitle">
            Critical Overdue (&gt;90d): <strong style={{ color: "#f87171" }}>₹{(data.finance.critical_overdue_90d / 1000).toFixed(0)}k</strong>
          </div>
          <div style={{ marginTop: "12px", fontSize: "0.8rem", color: "#fca5a5" }}>
            {data.finance.critical_debtor_count} high-risk debtor accounts flagged
          </div>
        </div>

        {/* Procurement Inventory Card */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <span className="card-title">Inventory & Stock Alerts</span>
            <Package size={20} color="#fbbf24" />
          </div>
          <div className="card-value" style={{ color: data.procurement.low_stock_skus_count > 0 ? "#fbbf24" : "#f8fafc" }}>
            {data.procurement.low_stock_skus_count} Low Stock
          </div>
          <div className="card-subtitle">{data.procurement.total_skus} active commercial catalog SKUs</div>
          <div style={{ marginTop: "12px", fontSize: "0.8rem", color: "#fde68a" }}>
            Deficit: <strong>{data.procurement.alerts.join(", ")}</strong>
          </div>
        </div>

        {/* Logistics & Dispatch Card */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <span className="card-title">Logistics & Shipments</span>
            <Truck size={20} color="#a78bfa" />
          </div>
          <div className="card-value">{data.logistics.total_shipments} Active</div>
          <div className="card-subtitle">
            In Transit: {data.logistics.in_transit_count} consignments
          </div>
          {data.logistics.delayed_shipments_count > 0 ? (
            <div style={{ marginTop: "12px", fontSize: "0.8rem", color: "#f87171", display: "flex", alignItems: "center", gap: "6px" }}>
              <Clock size={14} />
              <span>{data.logistics.delayed_shipments_count} consignment delayed (Siliguri bypass)</span>
            </div>
          ) : (
            <div style={{ marginTop: "12px", fontSize: "0.8rem", color: "#34d399" }}>All dispatches on schedule</div>
          )}
        </div>
      </div>

      {/* Second Row: System Readiness & Milestone Highlights */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
        {/* HR & Milestones */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "16px" }}>
            <span style={{ fontWeight: 600, color: "#f8fafc" }}>People & HR Milestones Today</span>
            <Users size={18} color="#38bdf8" />
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px", fontSize: "0.9rem" }}>
            <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", backgroundColor: "#0f172a", borderRadius: "6px" }}>
              <span>Employee Birthday:</span>
              <strong style={{ color: "#38bdf8" }}>Dr. Debashis Roy (MD / CEO)</strong>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", backgroundColor: "#0f172a", borderRadius: "6px" }}>
              <span>Work Anniversary (5 Years):</span>
              <strong style={{ color: "#34d399" }}>Debanjan Mukherjee (Senior TM)</strong>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", backgroundColor: "#0f172a", borderRadius: "6px" }}>
              <span>October Payslips Batch:</span>
              <span className="badge badge-status-warning">Draft Staging (Unreleased)</span>
            </div>
          </div>
        </div>

        {/* LLM Engine Health */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "16px" }}>
            <span style={{ fontWeight: 600, color: "#f8fafc" }}>Inference & LLM Status</span>
            <CheckCircle size={18} color="#34d399" />
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px", fontSize: "0.9rem" }}>
            <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", backgroundColor: "#0f172a", borderRadius: "6px" }}>
              <span>Active Provider:</span>
              <span className="badge badge-provider">{data.provider_status.provider_name.toUpperCase()}</span>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", backgroundColor: "#0f172a", borderRadius: "6px" }}>
              <span>Model Identifier:</span>
              <strong>{data.provider_status.model_name}</strong>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", backgroundColor: "#0f172a", borderRadius: "6px" }}>
              <span>Operational Details:</span>
              <span style={{ color: "#94a3b8", fontSize: "0.8rem" }}>{data.provider_status.details}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
