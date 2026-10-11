"""Realistic Synthetic Pharmaceutical Business Fixtures.

All data contained herein is purely synthetic, created for testing and demonstration.
Never connects to live systems.
"""


# Reference snapshot date for deterministic evaluation: 2026-10-10
SNAPSHOT_DATE = "2026-10-10T00:00:00Z"
DATA_MODE = "synthetic"

# 1. Product Catalog & Manufacturers
PRODUCTS = [
    {
        "sku": "BR-AZI-500",
        "name": "Azithromycin 500mg Tablets",
        "category": "Anti-Infective",
        "composition": "Azithromycin IP 500mg",
        "manufacturer": "Bengal Remedies Mfg Plant 1",
        "unit_mrp": 120.0,
        "trade_price": 84.0,
        "cost_price": 52.0,
        "stock_units": 8400,
        "reorder_threshold": 3000,
        "lead_time_days": 14,
        "safety_stock": 1500,
    },
    {
        "sku": "BR-AMX-625",
        "name": "Amoxicillin & Potassium Clavulanate 625mg",
        "category": "Anti-Infective",
        "composition": "Amoxicillin 500mg + Clavulanic Acid 125mg",
        "manufacturer": "Zenith Pharma Labs",
        "unit_mrp": 210.0,
        "trade_price": 148.0,
        "cost_price": 105.0,
        "stock_units": 450,  # LOW STOCK EXCEPTION
        "reorder_threshold": 1500,
        "lead_time_days": 21,
        "safety_stock": 800,
    },
    {
        "sku": "BR-PAN-40",
        "name": "Pantoprazole Gastro-Resistant 40mg",
        "category": "Gastroenterology",
        "composition": "Pantoprazole Sodium IP 40mg",
        "manufacturer": "Bengal Remedies Mfg Plant 1",
        "unit_mrp": 95.0,
        "trade_price": 66.0,
        "cost_price": 38.0,
        "stock_units": 14200,
        "reorder_threshold": 4000,
        "lead_time_days": 10,
        "safety_stock": 2000,
    },
    {
        "sku": "BR-TEL-40",
        "name": "Telmisartan 40mg Tablets",
        "category": "Cardiovascular",
        "composition": "Telmisartan IP 40mg",
        "manufacturer": "Sterling Biocare",
        "unit_mrp": 115.0,
        "trade_price": 80.0,
        "cost_price": 46.0,
        "stock_units": 9100,
        "reorder_threshold": 2500,
        "lead_time_days": 12,
        "safety_stock": 1200,
    },
    {
        "sku": "BR-MET-500",
        "name": "Metformin Hydrochloride Sustained Release 500mg",
        "category": "Diabetology",
        "composition": "Metformin HCl IP 500mg SR",
        "manufacturer": "Apex Formulations",
        "unit_mrp": 45.0,
        "trade_price": 31.0,
        "cost_price": 18.0,
        "stock_units": 18500,
        "reorder_threshold": 5000,
        "lead_time_days": 10,
        "safety_stock": 2500,
    },
    {
        "sku": "BR-MON-LC",
        "name": "Montelukast 10mg + Levocetirizine 5mg",
        "category": "Respiratory",
        "composition": "Montelukast Sodium 10mg + Levocetirizine 5mg",
        "manufacturer": "Zenith Pharma Labs",
        "unit_mrp": 145.0,
        "trade_price": 102.0,
        "cost_price": 64.0,
        "stock_units": 6200,
        "reorder_threshold": 2000,
        "lead_time_days": 15,
        "safety_stock": 1000,
    },
]

# 2. Ethical Sales by HQ & Sales Representative
ETHICAL_SALES_HQ = [
    {
        "hq_id": "HQ-CCU-01",
        "hq_name": "Kolkata Central",
        "state": "West Bengal",
        "area_manager": "Subhash Ghosh",
        "target_mtd": 1250000.0,
        "achieved_mtd": 1342500.0,  # 107.4%
        "growth_yoy_pct": 14.8,
        "active_sales_reps": 4,
        "top_performing_rep": "Debanjan Mukherjee",
        "as_of_date": "2026-10-10",
    },
    {
        "hq_id": "HQ-NBU-02",
        "hq_name": "North Bengal (Siliguri)",
        "state": "West Bengal",
        "area_manager": "Prakash Ray",
        "target_mtd": 950000.0,
        "achieved_mtd": 864500.0,  # 91.0%
        "growth_yoy_pct": 6.2,
        "active_sales_reps": 3,
        "top_performing_rep": "Amit Roy",
        "as_of_date": "2026-10-10",
    },
    {
        "hq_id": "HQ-ASN-03",
        "hq_name": "Asansol & Durgapur",
        "state": "West Bengal",
        "area_manager": "Ramesh Banerjee",
        "target_mtd": 800000.0,
        "achieved_mtd": 818000.0,  # 102.3%
        "growth_yoy_pct": 11.5,
        "active_sales_reps": 2,
        "top_performing_rep": "Rahul Sharma",
        "as_of_date": "2026-10-10",
    },
    {
        "hq_id": "HQ-PAT-04",
        "hq_name": "Patna HQ",
        "state": "Bihar",
        "area_manager": "Vikas Tiwari",
        "target_mtd": 1100000.0,
        "achieved_mtd": 985000.0,  # 89.5%
        "growth_yoy_pct": 4.1,
        "active_sales_reps": 3,
        "top_performing_rep": "Sanjay Verma",
        "as_of_date": "2026-10-10",
    },
    {
        "hq_id": "HQ-RAN-05",
        "hq_name": "Ranchi HQ",
        "state": "Jharkhand",
        "area_manager": "Alok Kumar",
        "target_mtd": 750000.0,
        "achieved_mtd": 792000.0,  # 105.6%
        "growth_yoy_pct": 13.0,
        "active_sales_reps": 2,
        "top_performing_rep": "Priya Das",
        "as_of_date": "2026-10-10",
    },
]

# 3. Consolidated PCD Sales (Propaganda Cum Distribution / Franchise Network)
PCD_SALES = [
    {
        "distributor_id": "PCD-BENGAL-01",
        "distributor_name": "Bengal Pharma Distributors",
        "territory": "Howrah & Hooghly",
        "orders_count": 28,
        "total_sales_val": 1820000.0,
        "pending_order_val": 145000.0,
        "payment_terms_days": 21,
        "status": "active",
        "last_order_date": "2026-10-08",
    },
    {
        "distributor_id": "PCD-SUNRISE-02",
        "distributor_name": "Sun Rise PCD Pharma",
        "territory": "Malda & Dinajpur",
        "orders_count": 19,
        "total_sales_val": 1140000.0,
        "pending_order_val": 88000.0,
        "payment_terms_days": 30,
        "status": "active",
        "last_order_date": "2026-10-05",
    },
    {
        "distributor_id": "PCD-CAREPOINT-03",
        "distributor_name": "CarePoint Remedies",
        "territory": "Ranchi Rural",
        "orders_count": 14,
        "total_sales_val": 920000.0,
        "pending_order_val": 0.0,
        "payment_terms_days": 15,
        "status": "active",
        "last_order_date": "2026-09-28",
    },
    {
        "distributor_id": "PCD-APEX-04",
        "distributor_name": "Apex Healthline PCD",
        "territory": "Bhagalpur",
        "orders_count": 12,
        "total_sales_val": 780000.0,
        "pending_order_val": 110000.0,
        "payment_terms_days": 30,
        "status": "credit_watch",  # EXCEPTION: Overdue watch
        "last_order_date": "2026-10-02",
    },
]

# 4. Invoices & Billing Details with Costing & Free Goods
INVOICES = [
    {
        "invoice_no": "INV-2026-4401",
        "date": "2026-10-07",
        "customer_id": "CUST-KOL-101",
        "customer_name": "Apollo Chemist Kolkata",
        "gross_amount": 168000.0,
        "discount_amount": 8400.0,
        "net_amount": 159600.0,
        "cost_of_goods_sold": 98800.0,
        "sample_scheme_goods_cost": 4200.0,
        "gross_profit": 56600.0,  # 159600 - (98800 + 4200) = 56600
        "gross_margin_pct": 35.46,
        "status": "paid",
        "payment_mode": "NEFT",
    },
    {
        "invoice_no": "INV-2026-4402",
        "date": "2026-10-08",
        "customer_id": "CUST-SIL-204",
        "customer_name": "North Bengal Medical Stores",
        "gross_amount": 215000.0,
        "discount_amount": 12900.0,
        "net_amount": 202100.0,
        "cost_of_goods_sold": 131400.0,
        "sample_scheme_goods_cost": 7500.0,
        "gross_profit": 63200.0,
        "gross_margin_pct": 31.27,
        "status": "unpaid",
        "payment_mode": "Credit",
    },
    {
        "invoice_no": "INV-2026-4409",
        "date": "2026-10-09",
        "customer_id": "CUST-PAT-550",
        "customer_name": "Janata Pharmacy Patna",
        "gross_amount": 88000.0,
        "discount_amount": 8800.0,
        "net_amount": 79200.0,
        "cost_of_goods_sold": 62100.0,
        "sample_scheme_goods_cost": 9900.0,  # Exceptionally heavy free goods scheme
        "gross_profit": 7200.0,
        "gross_margin_pct": 9.09,  # LOW MARGIN EXCEPTION (<15%)
        "status": "unpaid",
        "payment_mode": "Credit",
    },
]

# 5. Debtors and Creditors (Financial Aging)
DEBTORS = [
    {
        "customer_id": "CUST-MED-301",
        "customer_name": "Medico Chemists Asansol",
        "total_outstanding": 142000.0,
        "bucket_0_30": 82000.0,
        "bucket_31_60": 60000.0,
        "bucket_61_90": 0.0,
        "bucket_over_90": 0.0,
        "credit_limit": 200000.0,
        "is_overdue": True,
        "as_of_date": "2026-10-10",
    },
    {
        "customer_id": "CUST-CITY-909",
        "customer_name": "City Life Hospital & Pharmacy",
        "total_outstanding": 385000.0,
        "bucket_0_30": 40000.0,
        "bucket_31_60": 50000.0,
        "bucket_61_90": 50000.0,
        "bucket_over_90": 245000.0,  # CRITICAL OVERDUE EXCEPTION (>90 days)
        "credit_limit": 250000.0,
        "is_overdue": True,
        "as_of_date": "2026-10-10",
    },
    {
        "customer_id": "CUST-KOL-101",
        "customer_name": "Apollo Chemist Kolkata",
        "total_outstanding": 95000.0,
        "bucket_0_30": 95000.0,
        "bucket_31_60": 0.0,
        "bucket_61_90": 0.0,
        "bucket_over_90": 0.0,
        "credit_limit": 300000.0,
        "is_overdue": False,
        "as_of_date": "2026-10-10",
    },
]

CREDITORS = [
    {
        "vendor_id": "VEND-ZEN-01",
        "vendor_name": "Zenith Pharma Labs",
        "total_payable": 640000.0,
        "due_date": "2026-10-25",
        "payment_status": "pending_approval",
        "terms": "Net 30",
    },
    {
        "vendor_id": "VEND-STE-02",
        "vendor_name": "Sterling Biocare",
        "total_payable": 410000.0,
        "due_date": "2026-10-18",
        "payment_status": "scheduled",
        "terms": "Net 30",
    },
]

# 6. Logistics & Deliveries
SHIPMENTS = [
    {
        "shipment_id": "SHP-2026-7710",
        "lr_number": "LR-TCI-99412",
        "transporter": "TCI Freight",
        "destination_hq": "Kolkata Central",
        "dispatch_date": "2026-10-08",
        "estimated_delivery": "2026-10-10",
        "status": "delivered",
        "carton_count": 45,
        "is_delayed": False,
    },
    {
        "shipment_id": "SHP-2026-8821",
        "lr_number": "LR-BLU-44021",
        "transporter": "BlueDart Express",
        "destination_hq": "North Bengal (Siliguri)",
        "dispatch_date": "2026-10-02",
        "estimated_delivery": "2026-10-06",  # EXCEPTION: Overdue delivery
        "status": "in_transit_delayed",
        "carton_count": 80,
        "is_delayed": True,
        "delay_reason": "Siliguri highway bypass landslide blockade",
    },
    {
        "shipment_id": "SHP-2026-8850",
        "lr_number": "LR-VRL-11099",
        "transporter": "VRL Logistics",
        "destination_hq": "Patna HQ",
        "dispatch_date": "2026-10-09",
        "estimated_delivery": "2026-10-13",
        "status": "in_transit",
        "carton_count": 60,
        "is_delayed": False,
    },
]

# 7. HR Records & Events
EMPLOYEES = [
    {
        "emp_id": "EMP-001",
        "name": "Dr. Debashis Roy",
        "department": "Executive",
        "designation": "Managing Director / CEO",
        "join_date": "2018-04-01",
        "dob": "1974-10-10",  # BIRTHDAY TODAY (2026-10-10)
    },
    {
        "emp_id": "EMP-014",
        "name": "Debanjan Mukherjee",
        "department": "Ethical Sales",
        "designation": "Senior Territory Manager",
        "join_date": "2021-10-10",  # WORK ANNIVERSARY TODAY (5 Years)
        "dob": "1992-06-15",
    },
    {
        "emp_id": "EMP-028",
        "name": "Priya Das",
        "department": "Ethical Sales",
        "designation": "Medical Representative",
        "join_date": "2024-03-01",
        "dob": "1996-12-04",
    },
]

PAYSLIP_BATCHES = [
    {
        "batch_id": "PAY-SEP-2026",
        "month": "September 2026",
        "employee_count": 64,
        "total_disbursement": 2480000.0,
        "status": "processed_and_released",
    },
    {
        "batch_id": "PAY-OCT-2026",
        "month": "October 2026",
        "employee_count": 65,
        "total_disbursement": 2520000.0,
        "status": "draft_staging",
    },
]

# 8. Synthetic WhatsApp Ingestion Messages
WHATSAPP_MESSAGES = [
    {
        "msg_id": "WA-2026-101",
        "group_name": "Bengal Remedies HQ Orders",
        "sender": "+91-9830012345 (Debanjan Mukherjee)",
        "timestamp": "2026-10-10T08:30:00Z",
        "message_type": "text",
        "text": "Urgent stock required for Apollo Chemist Kolkata: 500 strips Azithro 500mg, 300 strips Panto 40mg. Marg PO will be generated by 11am.",
        "verified_accounting_entry": False,
        "is_duplicate": False,
    },
    {
        "msg_id": "WA-2026-102",
        "group_name": "Bengal Remedies Logistics Support",
        "sender": "+91-9831154321 (Driver Ramesh)",
        "timestamp": "2026-10-10T09:15:00Z",
        "message_type": "text",
        "text": "Truck for LR-BLU-44021 held at checkpost near Siliguri, clearance expected by this evening.",
        "verified_accounting_entry": False,
        "is_duplicate": False,
    },
    {
        "msg_id": "WA-2026-102-DUP",
        "group_name": "Bengal Remedies Logistics Support",
        "sender": "+91-9831154321 (Driver Ramesh)",
        "timestamp": "2026-10-10T09:15:02Z",
        "message_type": "text",
        "text": "Truck for LR-BLU-44021 held at checkpost near Siliguri, clearance expected by this evening.",
        "verified_accounting_entry": False,
        "is_duplicate": True,  # DUPLICATE EXCEPTION
    },
]
