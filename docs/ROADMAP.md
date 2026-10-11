# Bengal Remedies Platform Evolution Roadmap

## Phase 1: Foundation (Current Release)
- **Status**: Completed
- **Deliverables**:
  - Modular monolith architecture with 12 logical layers.
  - Working CEO conversational agent with bounded LangGraph orchestration.
  - Standardized agent contracts (`BaseAgent`, `AgentManifest`, `AgentResult`).
  - 10 specialist agent modules with declared manifests and truthful readiness.
  - Realistic synthetic pharmaceutical datasets across sales, inventory, billing, finance, logistics, HR, and WhatsApp.
  - Decoupled mock integration adapters (Marg ERP, B2B Portal, WhatsApp).
  - Free local LLM abstraction supporting Ollama (`qwen3:4b`, `llama3.2:3b`) and deterministic Mock fallback.
  - End-to-end observability (correlation IDs, structured JSON logging, spans, telemetry metrics).
  - Explicit agent evaluation framework with 12 test cases across 9 categories.
  - Controlled continuous improvement engine with human-in-the-loop review gates.
  - Full React + TypeScript + Vite executive command center.

---

## Phase 2: Commercial Sales & Billing Deepening
- **Target**: Q1 2027
- **Focus**:
  - Live read-only Marg ERP database connector for real-time ledger synchronization.
  - Automated doctor coverage and medical representative (MR) daily call reporting ingestion.
  - Dynamic scheme free-goods leakage analyzer detecting promotional bonus erosion.
  - Territory rebalancing recommendation engine.

---

## Phase 3: Supply Chain & Procurement Operations
- **Target**: Q2 2027
- **Focus**:
  - Automated supplier Request For Quotation (RFQ) generation.
  - B2B ordering portal webhook ingestion pipeline.
  - Cold-chain temperature telemetry tracking for biopharmaceutical consignments.
  - Transporter SLA scoring and automated transit delay rerouting recommendations.

---

## Phase 4: Medical Affairs & Regulatory Automation
- **Target**: Q3 2027
- **Focus**:
  - CDSCO / DCGI regulatory dossier validation and Form 40 check automation.
  - Medical literature semantic RAG for contraindications and drug interactions.
  - Digital LBL brochure builder with automated medical review routing.

---

## Phase 5: Long-Term Semantic Memory & Domain Fine-Tuning
- **Target**: Q4 2027
- **Focus**:
  - Enterprise document vector indexing for SOPs and clinical trial documentation.
  - Offline LoRA fine-tuning of open-weights models for specialized Indian pharmaceutical terminology and Marg ERP accounting codes.
  - Multi-tenant enterprise deployment on private Kubernetes clusters.
