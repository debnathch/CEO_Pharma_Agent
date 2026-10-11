# Security, Privacy & Governance Architecture

## 1. Security Principles

The platform processes sensitive pharmaceutical operational, financial, and personnel data. The architecture enforces zero-trust boundaries, input sanitization, prompt injection defenses, and strict write isolation.

---

## 2. Key Security Mechanisms

### 1. Write Isolation (Zero Direct Production Writes)
In this foundation phase, the multi-agent ecosystem is strictly **read-only**:
- `submit_purchase_order` in `ProcurementAgent` returns `not_implemented` (requires approval).
- `execute_payment_run` in `FinanceAgent` returns `not_implemented` (requires approval).
- `publish_campaign_externally` in `MarketingAgent` returns `not_implemented`.
- `transmit_employee_payslips` in `HRAgent` returns `not_implemented`.
Natural language instructions from chat users **cannot** override this programmatic access-control boundary.

### 2. Prompt Injection Defenses
Untrusted external inputs (such as synthetic WhatsApp messages, driver transcripts, or OCR text) are treated as data payloads, never as system instructions:
- External message content is encapsulated inside explicit JSON data containers.
- The CEO Master Agent prompt explicitly separates `User Query` from `Verified Business Evidence`.
- High-risk keywords (e.g. `"ignore previous instructions"`, `"transfer funds"`) are isolated and cannot alter agent execution plans.

### 3. PII & Sensitive Data Redaction
- In structured JSON logs, sensitive credentials, raw bank account details, and unredacted payslip components are scrubbed before logging.
- Telemetry events log only metadata (`duration_ms`, `agent_id`, `status`, `event_type`), never sensitive payloads.

### 4. Agent & Tool Permission Scopes
Each agent declares its required permission scopes:
- `sales:read`
- `inventory:read`
- `billing:read`
- `finance:read`
- `logistics:read`
- `hr:read`
- `executive:all`
Future capabilities that perform mutations will require the `write` or `admin` permission role verified by the API security middleware.

### 5. Regulatory Disclaimers
Any generated marketing literature or Leave Behind Literature (LBL) produced by `ProductLaunchAgent` is programmatically attached with mandatory regulatory notices:
> *"IMPORTANT REGULATORY DISCLAIMER: Internal draft only. NOT approved by CDSCO/DCGI. Dissemination to physicians prohibited prior to medical-legal sign-off."*
