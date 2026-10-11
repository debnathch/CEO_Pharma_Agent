# Specialist Agent Catalog

This catalog documents the declared manifests, domains, versions, capabilities, and readiness statuses for all 10 specialist agents in the Bengal Remedies ecosystem.

---

## 1. CEO Master Agent (`ceo_master`)
- **Display Name**: CEO Master Intelligence Agent
- **Domain**: Executive Leadership
- **Version**: `0.1.0`
- **Implementation Status**: `FULL`
- **Required Permissions**: `executive:all`
- **Supported Tools**: `all_specialist_agents`, `orchestration_engine`
- **Description**: Executive orchestration, natural language conversational query processing, cross-domain evidence grounding, and morning daily briefings.
- **Capabilities**:
  - `handle_chat_query` [Implemented: YES]: Classifies intent, discovers specialists dynamically, aggregates results, and generates grounded summaries.
  - `generate_daily_briefing` [Implemented: YES]: Multi-agent synthesis combining sales, operations, finance, procurement, and HR milestones.

---

## 2. Ethical Sales Agent (`ethical_sales`)
- **Display Name**: Ethical Pharmaceutical Sales Agent
- **Domain**: Ethical Sales
- **Version**: `0.1.0`
- **Implementation Status**: `PARTIAL`
- **Required Permissions**: `sales:read`
- **Supported Tools**: `sales_service`
- **Description**: Analyzes HQ-wise sales, salesperson target achievement, and medical representative field coverage.
- **Capabilities**:
  - `get_hq_sales_summary` [Implemented: YES]: Computes MTD sales targets, achievements, and top/lowest performing HQs.
  - `get_hq_detail` [Implemented: YES]: Detailed performance for a specific HQ (Kolkata, Siliguri, Asansol, Patna, Ranchi).
  - `ingest_field_reports` [Implemented: NO - SKELETON]: Ingestion of doctor call reports and daily activity (returns truthful `not_implemented`).

---

## 3. PCD Sales Agent (`pcd_sales`)
- **Display Name**: PCD Franchise Sales Agent
- **Domain**: PCD Distribution
- **Version**: `0.1.0`
- **Implementation Status**: `PARTIAL`
- **Required Permissions**: `pcd:read`
- **Supported Tools**: `sales_service`
- **Description**: Manages PCD franchise distribution network, distributor order standings, and pending pipeline.
- **Capabilities**:
  - `get_pcd_sales_summary` [Implemented: YES]: Consolidated PCD revenue, order count, and distributor standings.
  - `analyze_distributor_trends` [Implemented: NO - SKELETON]: Deep franchise territory trend analysis.

---

## 4. Procurement Agent (`procurement`)
- **Display Name**: Procurement & Inventory Agent
- **Domain**: Procurement & Supply Chain
- **Version**: `0.1.0`
- **Implementation Status**: `PARTIAL`
- **Required Permissions**: `inventory:read`
- **Supported Tools**: `procurement_service`
- **Description**: Identifies stock levels below safety reorder thresholds, computes suggested order units, and manufacturer lead times.
- **Capabilities**:
  - `get_inventory_alerts` [Implemented: YES]: Flags critical low-stock SKUs and suggests reorder units.
  - `compare_manufacturers` [Implemented: NO - SKELETON]: Compares manufacturer quotations and lead times.
  - `submit_purchase_order` [Implemented: NO - RESTRICTED]: High-risk write operation requiring human executive sign-off.

---

## 5. Billing Agent (`billing`)
- **Display Name**: Billing & Gross Profit Agent
- **Domain**: Billing & Commercial
- **Version**: `0.1.0`
- **Implementation Status**: `PARTIAL`
- **Required Permissions**: `billing:read`
- **Supported Tools**: `billing_service`
- **Description**: Performs deterministic billing calculations, gross profit audits, and sample/bonus goods impact analysis.
- **Capabilities**:
  - `get_billing_summary` [Implemented: YES]: Computes net billed revenue, COGS, free goods costs, and overall gross margin percentage.
  - `analyze_free_goods_leakage` [Implemented: NO - SKELETON]: Detects unapproved physician bonus goods erosion.

---

## 6. Finance Agent (`finance`)
- **Display Name**: Finance & Accounts Agent
- **Domain**: Finance & Accounts
- **Version**: `0.1.0`
- **Implementation Status**: `PARTIAL`
- **Required Permissions**: `finance:read`
- **Supported Tools**: `finance_service`
- **Description**: Audits accounts receivable aging buckets (0-30, 31-60, 61-90, >90), critical overdue balances, and trade creditors.
- **Capabilities**:
  - `get_debtors_aging` [Implemented: YES]: Classifies debtor balances and highlights overdue debtors exceeding credit limits.
  - `get_creditors_summary` [Implemented: YES]: Summarizes manufacturer supplier payables.
  - `execute_payment_run` [Implemented: NO - RESTRICTED]: High-risk banking disbursement.

---

## 7. Logistics Agent (`logistics`)
- **Display Name**: Logistics & Delivery Tracking Agent
- **Domain**: Logistics & Supply Chain
- **Version**: `0.1.0`
- **Implementation Status**: `PARTIAL`
- **Required Permissions**: `logistics:read`
- **Supported Tools**: `logistics_service`
- **Description**: Tracks dispatches from warehouse, consignment LR numbers, and active transport delays.
- **Capabilities**:
  - `get_shipments_status` [Implemented: YES]: Audits active dispatches, delivered orders, and detects transit delays.
  - `reroute_delayed_shipment` [Implemented: NO - RESTRICTED]: Emergency dispatch rerouting.

---

## 8. Marketing Agent (`marketing`)
- **Display Name**: Digital Marketing Agent
- **Domain**: Marketing & Brand
- **Version**: `0.1.0`
- **Implementation Status**: `PARTIAL`
- **Required Permissions**: `marketing:read`
- **Supported Tools**: `marketing_service`
- **Description**: Drafts medical promotional campaigns, physician digital engagement, and educational briefs.
- **Capabilities**:
  - `get_campaign_drafts` [Implemented: YES]: Retrieves staged digital marketing campaigns with sandbox indicators.
  - `publish_campaign_externally` [Implemented: NO - RESTRICTED]: External publishing to social media (disabled by design).

---

## 9. Product Launch Agent (`product_launch`)
- **Display Name**: Product Launch & LBL Agent
- **Domain**: Medical Affairs & Product Management
- **Version**: `0.1.0`
- **Implementation Status**: `PARTIAL`
- **Required Permissions**: `product:read`
- **Supported Tools**: `product_service`
- **Description**: Manages new product introduction pipeline, product cards, and Leave Behind Literature (LBL) drafts.
- **Capabilities**:
  - `get_launch_pipeline` [Implemented: YES]: Retrieves upcoming molecule launches and literature drafting status.
  - `generate_lbl_draft` [Implemented: YES]: Generates unapproved doctor LBL brochures with mandatory regulatory disclaimers.

---

## 10. HR Agent (`hr`)
- **Display Name**: Human Resources Agent
- **Domain**: Human Resources
- **Version**: `0.1.0`
- **Implementation Status**: `PARTIAL`
- **Required Permissions**: `hr:read`
- **Supported Tools**: `hr_service`
- **Description**: Manages employee milestones, birthdays, work anniversaries, recruitment pipeline, and payslip staging.
- **Capabilities**:
  - `get_milestones_and_payslips` [Implemented: YES]: Identifies birthdays, work anniversaries, and payslip batch staging status.
  - `transmit_employee_payslips` [Implemented: NO - RESTRICTED]: Bulk transmission of employee payslips (disabled by design).
