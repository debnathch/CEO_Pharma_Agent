import React, { useState } from "react";
import { Send, Bot, User, ShieldCheck, ChevronDown, ChevronUp, ThumbsUp, ThumbsDown, Sparkles } from "lucide-react";
import { sendChatMessage, submitFeedback } from "../services/api.ts";
import { ChatMessage } from "../types.ts";

export const CEOChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "intro-01",
      sender: "ceo",
      text: "Good morning, Dr. Roy. I am your CEO Master Intelligence Agent. I have active bounded orchestration access to ethical sales, PCD franchise distribution, procurement, billing, finance, logistics, product introduction, and HR records. How may I assist your executive decisions today?",
      timestamp: new Date().toLocaleTimeString(),
      agentsInvoked: ["ceo_master"],
      isMock: true,
      providerUsed: "mock",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [expandedEvidence, setExpandedEvidence] = useState<Record<string, boolean>>({});
  const [feedbackSent, setFeedbackSent] = useState<Record<string, string>>({});

  const suggestedPrompts = [
    "How is Kolkata HQ sales performing this month?",
    "Which pharmaceutical stocks are below safety reorder threshold?",
    "Show me overdue debtors and accounts receivable aging",
    "Are any dispatches delayed or held up in transit?",
    "What is our total invoiced sales, gross profit, and gross margin?",
    "Give me the comprehensive CEO daily morning briefing",
  ];

  const handleSend = async (queryText?: string) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: textToSend,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!queryText) setInput("");
    setLoading(true);

    try {
      const res = await sendChatMessage(textToSend);
      const ceoMsg: ChatMessage = {
        id: `ceo-${Date.now()}`,
        sender: "ceo",
        text: res.summary,
        timestamp: new Date().toLocaleTimeString(),
        agentsInvoked: res.agents_invoked,
        evidence: res.evidence,
        warnings: res.warnings,
        durationMs: res.duration_ms,
        providerUsed: res.provider_used,
        isMock: res.is_mock,
        executionId: res.execution_id,
      };
      setMessages((prev) => [...prev, ceoMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        sender: "ceo",
        text: `Error connecting to orchestration workflow: ${err.message}`,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (executionId: string, rating: string) => {
    try {
      await submitFeedback(executionId, rating, `Review submitted from CEO chat interface (${rating})`);
      setFeedbackSent((prev) => ({ ...prev, [executionId]: rating }));
    } catch (err) {
      console.error(err);
    }
  };

  const toggleEvidence = (msgId: string) => {
    setExpandedEvidence((prev) => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  return (
    <div className="chat-container">
      {/* Header Banner */}
      <div style={{ padding: "12px 20px", borderBottom: "1px solid #334155", display: "flex", justifyContent: "space-between", alignItems: "center", backgroundColor: "#0f172a" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <ShieldCheck size={18} color="#38bdf8" />
          <span style={{ fontSize: "0.85rem", color: "#94a3b8" }}>
            Bounded B2B Multi-Agent Orchestration • Grounded on Synthetic Business Records
          </span>
        </div>
        <span className="badge badge-synthetic">MOCK / LOCAL LLM MODE</span>
      </div>

      {/* Messages Feed */}
      <div className="chat-messages">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`chat-bubble ${msg.sender === "user" ? "chat-bubble-user" : "chat-bubble-ceo"}`}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
              {msg.sender === "user" ? <User size={16} /> : <Bot size={16} color="#38bdf8" />}
              <strong style={{ fontSize: "0.85rem" }}>{msg.sender === "user" ? "Dr. Roy (CEO)" : "CEO Master Agent"}</strong>
              <span style={{ fontSize: "0.75rem", opacity: 0.7, marginLeft: "auto" }}>{msg.timestamp}</span>
            </div>

            <div style={{ whiteSpace: "pre-line" }}>{msg.text}</div>

            {/* Invoked Specialist Pills */}
            {msg.agentsInvoked && msg.agentsInvoked.length > 0 && (
              <div style={{ marginTop: "12px", display: "flex", flexWrap: "wrap", gap: "6px", alignItems: "center" }}>
                <span style={{ fontSize: "0.75rem", color: "#94a3b8" }}>Agents Discovered &amp; Invoked:</span>
                {msg.agentsInvoked.map((a) => (
                  <span
                    key={a}
                    style={{
                      fontSize: "0.75rem",
                      backgroundColor: "#1e293b",
                      border: "1px solid #475569",
                      padding: "2px 8px",
                      borderRadius: "4px",
                      color: "#38bdf8",
                    }}
                  >
                    {a}
                  </span>
                ))}
              </div>
            )}

            {/* Warnings */}
            {msg.warnings && msg.warnings.length > 0 && (
              <div style={{ marginTop: "10px", padding: "8px 12px", backgroundColor: "#451a03", border: "1px solid #b45309", borderRadius: "6px", fontSize: "0.8rem", color: "#fef3c7" }}>
                {msg.warnings.map((w, idx) => (
                  <div key={idx}>⚠️ {w}</div>
                ))}
              </div>
            )}

            {/* Evidence Drawer Toggle */}
            {msg.evidence && msg.evidence.length > 0 && (
              <div style={{ marginTop: "12px" }}>
                <button
                  onClick={() => toggleEvidence(msg.id)}
                  style={{
                    background: "none",
                    border: "none",
                    color: "#94a3b8",
                    fontSize: "0.8rem",
                    display: "flex",
                    alignItems: "center",
                    gap: "4px",
                    cursor: "pointer",
                    padding: 0,
                  }}
                >
                  {expandedEvidence[msg.id] ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                  <span>{expandedEvidence[msg.id] ? "Hide Evidence Chain" : `View Evidence Chain (${msg.evidence.length} records)`}</span>
                </button>

                {expandedEvidence[msg.id] && (
                  <div style={{ marginTop: "8px", padding: "10px", backgroundColor: "#0f172a", borderRadius: "6px", fontSize: "0.75rem", border: "1px solid #334155" }}>
                    {msg.evidence.map((ev, i) => (
                      <div key={i} style={{ marginBottom: "6px", borderBottom: i < msg.evidence!.length - 1 ? "1px solid #1e293b" : "none", paddingBottom: "4px" }}>
                        <div style={{ color: "#38bdf8", fontWeight: 600 }}>Source: {ev.source_system} ({ev.authoritative ? "Authoritative" : "Non-Authoritative"})</div>
                        <div style={{ color: "#cbd5e1" }}>Entity: {ev.entity_type} (ID: {ev.entity_id})</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Feedback & Trace Footer */}
            {msg.sender === "ceo" && msg.executionId && (
              <div style={{ marginTop: "14px", paddingTop: "8px", borderTop: "1px solid #475569", display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: "0.75rem", color: "#94a3b8" }}>
                <div>
                  Trace: <code>{msg.executionId}</code> {msg.durationMs ? `(${msg.durationMs}ms)` : ""}
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  <span>Review quality:</span>
                  {feedbackSent[msg.executionId] ? (
                    <span style={{ color: "#34d399", fontWeight: 600 }}>Recorded ({feedbackSent[msg.executionId]})</span>
                  ) : (
                    <>
                      <button
                        onClick={() => handleFeedback(msg.executionId!, "helpful")}
                        title="Mark Helpful"
                        style={{ background: "none", border: "none", color: "#94a3b8", cursor: "pointer" }}
                      >
                        <ThumbsUp size={14} />
                      </button>
                      <button
                        onClick={() => handleFeedback(msg.executionId!, "incorrect")}
                        title="Mark Incorrect"
                        style={{ background: "none", border: "none", color: "#94a3b8", cursor: "pointer" }}
                      >
                        <ThumbsDown size={14} />
                      </button>
                    </>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="chat-bubble chat-bubble-ceo" style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <Sparkles size={16} color="#38bdf8" className="animate-spin" />
            <span style={{ color: "#94a3b8" }}>Synthesizing multi-agent intelligence...</span>
          </div>
        )}
      </div>

      {/* Suggested Prompt Chips */}
      <div className="suggested-chips">
        {suggestedPrompts.map((p, idx) => (
          <button key={idx} className="chip" onClick={() => handleSend(p)} disabled={loading}>
            {p}
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <div className="chat-input-bar">
        <input
          type="text"
          className="chat-input"
          placeholder="Ask CEO intelligence agent (e.g. sales, inventory alerts, overdue debtor risk, dispatches)..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          disabled={loading}
        />
        <button className="btn-primary" onClick={() => handleSend()} disabled={loading || !input.trim()}>
          <Send size={18} />
        </button>
      </div>
    </div>
  );
};
