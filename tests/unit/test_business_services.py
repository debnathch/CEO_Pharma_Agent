"""Unit tests for deterministic business services."""

from pharma_platform.business_services import (
    BillingService,
    FinanceService,
    HRService,
    LogisticsService,
    ProcurementService,
    SalesService,
)


def test_sales_service_ethical_summary():
    summary = SalesService.get_ethical_sales_summary()
    assert summary["hq_count"] == 5
    assert summary["overall_achievement_pct"] > 0
    assert summary["total_achieved_mtd"] > 0
    assert summary["total_target_mtd"] > 0
    assert summary["top_performing_hq"] == "Kolkata Central"


def test_sales_service_hq_lookup():
    kolkata = SalesService.get_hq_sales_by_id_or_name("Kolkata")
    assert kolkata is not None
    assert kolkata["hq_id"] == "HQ-CCU-01"
    assert kolkata["achievement_pct"] == 107.4

    unknown = SalesService.get_hq_sales_by_id_or_name("NonExistentHQ")
    assert unknown is None


def test_sales_service_pcd_summary():
    summary = SalesService.get_pcd_sales_summary()
    assert summary["distributor_count"] == 4
    assert summary["total_revenue"] > 0
    assert summary["total_pending_orders_val"] > 0


def test_billing_service_deterministic_calculations():
    summary = BillingService.get_billing_summary()
    assert summary["invoice_count"] == 3
    assert summary["total_invoiced_net"] == 440900.0
    assert summary["total_cogs"] == 292300.0
    assert summary["total_free_goods_cost"] == 21600.0
    assert summary["total_gross_profit"] == 127000.0
    assert summary["overall_gross_margin_pct"] == 28.8
    assert summary["low_margin_invoices_count"] == 1
    assert summary["low_margin_alerts"][0]["invoice_no"] == "INV-2026-4409"
    assert summary["low_margin_alerts"][0]["gross_margin_pct"] == 9.09


def test_finance_service_aging_buckets():
    debtors = FinanceService.get_debtors_aging_summary()
    assert debtors["debtor_count"] == 3
    assert debtors["total_debtors_outstanding"] == 622000.0
    assert debtors["aging_buckets"]["days_over_90"] == 245000.0
    assert debtors["critical_risk_count"] >= 1
    assert any("City Life Hospital" in d["customer_name"] for d in debtors["critical_risk_debtors"])

    creditors = FinanceService.get_creditors_summary()
    assert creditors["creditor_count"] == 2
    assert creditors["total_creditors_payable"] == 1050000.0


def test_procurement_service_stock_deficit():
    inventory = ProcurementService.get_inventory_status()
    assert inventory["total_skus"] == 6
    assert inventory["low_stock_skus_count"] == 1
    alert_item = inventory["low_stock_alerts"][0]
    assert alert_item["sku"] == "BR-AMX-625"
    assert alert_item["current_stock"] == 450
    assert alert_item["reorder_threshold"] == 1500
    assert alert_item["suggested_reorder_units"] == 1850


def test_logistics_service_transit_delays():
    logistics = LogisticsService.get_shipments_summary()
    assert logistics["total_shipments"] == 3
    assert logistics["delayed_shipments_count"] == 1
    delayed = logistics["delayed_shipments"][0]
    assert delayed["shipment_id"] == "SHP-2026-8821"
    assert delayed["is_delayed"] is True


def test_hr_service_milestones():
    hr = HRService.get_milestones_and_batches()
    assert hr["total_employees"] == 3
    assert len(hr["birthdays_today"]) == 1
    assert hr["birthdays_today"][0]["name"] == "Dr. Debashis Roy"
    assert len(hr["anniversaries_today"]) == 1
    assert hr["anniversaries_today"][0]["name"] == "Debanjan Mukherjee"
