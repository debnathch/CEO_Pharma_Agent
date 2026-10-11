import React, { useState } from "react";
import {
  LayoutDashboard,
  MessageSquare,
  Cpu,
  Share2,
  History,
  Activity,
  ShieldCheck,
  GitBranch,
  CheckSquare,
} from "lucide-react";
import { OverviewPage } from "./pages/OverviewPage.tsx";
import { CEOChatPage } from "./pages/CEOChatPage.tsx";
import { AgentDirectoryPage } from "./pages/AgentDirectoryPage.tsx";
import { IntegrationsPage } from "./pages/IntegrationsPage.tsx";
import { ExecutionsPage } from "./pages/ExecutionsPage.tsx";
import { ObservabilityPage } from "./pages/ObservabilityPage.tsx";
import { EvaluationPage } from "./pages/EvaluationPage.tsx";
import { ImprovementPage } from "./pages/ImprovementPage.tsx";
import { ApprovalsPage } from "./pages/ApprovalsPage.tsx";

type NavTab =
  | "overview"
  | "chat"
  | "agents"
  | "integrations"
  | "executions"
  | "observability"
  | "evaluation"
  | "improvement"
  | "approvals";

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavTab>("overview");

  const navItems: { id: NavTab; label: string; icon: React.ReactNode }[] = [
    { id: "overview", label: "Business Overview", icon: <LayoutDashboard size={18} /> },
    { id: "chat", label: "CEO Intelligence Chat", icon: <MessageSquare size={18} /> },
    { id: "agents", label: "Specialist Agents", icon: <Cpu size={18} /> },
    { id: "integrations", label: "Integrations", icon: <Share2 size={18} /> },
    { id: "executions", label: "Execution History", icon: <History size={18} /> },
    { id: "observability", label: "Observability", icon: <Activity size={18} /> },
    { id: "evaluation", label: "Agent Evaluation", icon: <ShieldCheck size={18} /> },
    { id: "improvement", label: "Improvement Proposals", icon: <GitBranch size={18} /> },
    { id: "approvals", label: "Simulated Approvals", icon: <CheckSquare size={18} /> },
  ];

  const getPageTitle = () => {
    switch (activeTab) {
      case "overview":
        return "Executive Business Dashboard";
      case "chat":
        return "CEO Master Conversational Agent";
      case "agents":
        return "Specialist Agent Directory & Manifests";
      case "integrations":
        return "Enterprise Integration Adapters (Mock)";
      case "executions":
        return "Platform Execution & Trace History";
      case "observability":
        return "Telemetry, Latency & Error Observability";
      case "evaluation":
        return "Quality Measurement & Regression Evaluation";
      case "improvement":
        return "Controlled Continuous Improvement Workflow";
      case "approvals":
        return "High-Risk Operation Approval Queue";
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div style={{ width: "32px", height: "32px", borderRadius: "8px", backgroundColor: "#0284c7", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold" }}>
            BR
          </div>
          <div>
            <h2>Bengal Remedies</h2>
            <div style={{ fontSize: "0.75rem", color: "#64748b" }}>CEO Multi-Agent AI</div>
          </div>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${activeTab === item.id ? "active" : ""}`}
              onClick={() => setActiveTab(item.id)}
            >
              {item.icon}
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div>Platform: <strong>v0.1.0</strong> (Foundation)</div>
          <div style={{ marginTop: "4px", color: "#475569" }}>Engine: Modular Monolith</div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <header className="top-header">
          <div className="header-title">
            <h1>{getPageTitle()}</h1>
          </div>
          <div className="header-badges">
            <span className="badge badge-synthetic">SYNTHETIC DATA</span>
            <span className="badge badge-provider">MOCK / OLLAMA READY</span>
            <span className="badge badge-status-online">SYSTEM HEALTHY</span>
          </div>
        </header>

        <div className="page-body">
          {activeTab === "overview" && <OverviewPage />}
          {activeTab === "chat" && <CEOChatPage />}
          {activeTab === "agents" && <AgentDirectoryPage />}
          {activeTab === "integrations" && <IntegrationsPage />}
          {activeTab === "executions" && <ExecutionsPage />}
          {activeTab === "observability" && <ObservabilityPage />}
          {activeTab === "evaluation" && <EvaluationPage />}
          {activeTab === "improvement" && <ImprovementPage />}
          {activeTab === "approvals" && <ApprovalsPage />}
        </div>
      </main>
    </div>
  );
};

export default App;
