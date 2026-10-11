# External System Integration Boundaries

## 1. Integration Boundary Architecture

The platform interfaces with several existing enterprise systems via dedicated adapters (`src/pharma_platform/integrations/`). In the foundation phase, **all adapters run in synthetic mock mode**. No calls are made to live corporate portals or production database servers.

---

## 2. Integration Catalog

### 1. Marg ERP (`marg_erp`)
- **Authority**: Authoritative source of truth for General Ledger, Invoices, COGS, Accounts Receivable (Debtors), and Accounts Payable (Creditors).
- **Status**: Mock Synthetic Adapter.
- **Data Provided**:
  - `fetch_invoices()`: Line item details, trade discounts, cost price, scheme free-goods cost.
  - `fetch_debtors()`: Customer accounts with aging buckets (0-30, 31-60, 61-90, >90).
  - `fetch_creditors()`: Vendor payables and terms.

### 2. Bengal Remedies B2B Ordering Portal (`ordering_portal`)
- **Reference URL**: `http://bengalremedies.com:9000/` (Mocked; live calls disabled).
- **Authority**: Authoritative source for PCD franchise order intake and dispatch staging.
- **Status**: Mock Synthetic Adapter.
- **Data Provided**:
  - `fetch_pcd_orders()`: Distributor orders, pending order pipeline, and credit watch status.

### 3. WhatsApp Field Group Feeds (`whatsapp_ingest`)
- **Authority**: Strictly **non-authoritative evidence**. WhatsApp messages represent informal field reports, driver transit updates, or order inquiries. They do not constitute accounting entries until entered into Marg ERP.
- **Status**: Mock Synthetic Adapter.
- **Idempotency & Deduplication**:
  - Field feeds frequently contain re-sent or duplicated messages (e.g. `WA-2026-102` vs `WA-2026-102-DUP`).
  - `WhatsAppIngestionAdapter.fetch_imported_messages(exclude_duplicates=True)` hashes `sender + text` to guarantee idempotent message processing.
- **Unofficial Scraping Disclaimer**: The platform **never** uses unofficial browser scraping (e.g. WhatsApp Web automation via Selenium/Playwright) to avoid credential theft, account bans, and un-audited access. All imports must pass through official webhook endpoints or verified synthetic batches.

### 4. Digital Marketing Channels (`social_media`)
- **Authority**: Read-only campaign draft staging.
- **Status**: Mock Sandbox. External publishing is strictly disabled.

### 5. HR Employee Records (`hr_records`)
- **Authority**: Employee profiles, designations, milestones, and payslip templates.
- **Status**: Mock Synthetic Adapter. Real employee documents and PII are never processed or transmitted.
