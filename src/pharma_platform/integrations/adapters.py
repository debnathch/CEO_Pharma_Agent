"""Mock Integration Adapters for Enterprise Pharmaceutical Systems.

Strictly synthetic. Clearly documents ownership boundaries.
"""

from typing import Any

from pharma_platform.data.synthetic.fixtures import (
    CREDITORS,
    DEBTORS,
    EMPLOYEES,
    INVOICES,
    PCD_SALES,
    WHATSAPP_MESSAGES,
)
from pharma_platform.integrations.base_adapter import BaseIntegrationAdapter, IntegrationHealth


class MargERPAdapter(BaseIntegrationAdapter):
    """Adapter for Marg ERP. Authority for general ledger, invoicing, and accounting."""

    def get_system_id(self) -> str:
        return "marg_erp"

    def get_health(self) -> IntegrationHealth:
        return IntegrationHealth(
            system_id="marg_erp",
            display_name="Marg ERP Accounting System",
            is_connected=True,
            is_mock=True,
            authority_scope="Accounting, General Ledger, Invoices, Debtor/Creditor Balances",
            status_message="Connected (Synthetic Mock Adapter)",
        )

    def fetch_invoices(self) -> list[dict[str, Any]]:
        return INVOICES

    def fetch_debtors(self) -> list[dict[str, Any]]:
        return DEBTORS

    def fetch_creditors(self) -> list[dict[str, Any]]:
        return CREDITORS


class OrderingPortalAdapter(BaseIntegrationAdapter):
    """Adapter for B2B Ordering Portal (http://bengalremedies.com:9000). Authority for order intake and franchise orders."""

    def get_system_id(self) -> str:
        return "ordering_portal"

    def get_health(self) -> IntegrationHealth:
        return IntegrationHealth(
            system_id="ordering_portal",
            display_name="Bengal Remedies B2B Ordering Portal",
            is_connected=True,
            is_mock=True,
            authority_scope="Order Submission, PCD Franchise Order Workflow, Pending Approvals",
            status_message="Connected (Synthetic Mock Adapter - Live connection disabled)",
        )

    def fetch_pcd_orders(self) -> list[dict[str, Any]]:
        return PCD_SALES


class WhatsAppIngestionAdapter(BaseIntegrationAdapter):
    """Adapter for WhatsApp Group Ingestions. Synthetic input source only (Not authoritative accounting data)."""

    def get_system_id(self) -> str:
        return "whatsapp_ingest"

    def get_health(self) -> IntegrationHealth:
        return IntegrationHealth(
            system_id="whatsapp_ingest",
            display_name="WhatsApp Field Group Ingestion Feed",
            is_connected=True,
            is_mock=True,
            authority_scope="Unstructured Evidence, Field Notes, Voice Transcriptions (Non-Authoritative)",
            status_message="Connected (Synthetic imported fixture events)",
        )

    def fetch_imported_messages(self, exclude_duplicates: bool = True) -> list[dict[str, Any]]:
        """Return synthetic messages with idempotent deduplication."""
        if exclude_duplicates:
            seen_hashes = set()
            deduped = []
            for msg in WHATSAPP_MESSAGES:
                h = f"{msg['sender']}:{msg['text']}"
                if h not in seen_hashes:
                    seen_hashes.add(h)
                    deduped.append(msg)
            return deduped
        return WHATSAPP_MESSAGES


class SocialMediaAdapter(BaseIntegrationAdapter):
    """Adapter for Social Media Campaigns. Simulated drafts only (No external publishing)."""

    def get_system_id(self) -> str:
        return "social_media"

    def get_health(self) -> IntegrationHealth:
        return IntegrationHealth(
            system_id="social_media",
            display_name="Digital Marketing & Social Channels",
            is_connected=True,
            is_mock=True,
            authority_scope="Campaign Drafts, Simulated Analytics (Publishing Disabled)",
            status_message="Connected (Simulated Draft Sandbox)",
        )


class HRSystemAdapter(BaseIntegrationAdapter):
    """Adapter for HR Employee Records."""

    def get_system_id(self) -> str:
        return "hr_records"

    def get_health(self) -> IntegrationHealth:
        return IntegrationHealth(
            system_id="hr_records",
            display_name="HR Files & Employee Roster",
            is_connected=True,
            is_mock=True,
            authority_scope="Employee Profiles, Announcements, Payslip Staging",
            status_message="Connected (Synthetic HR Repository)",
        )

    def fetch_employees(self) -> list[dict[str, Any]]:
        return EMPLOYEES
