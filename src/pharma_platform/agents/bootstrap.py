"""Bootstrap and register all agents in the platform ecosystem."""

import logging

from pharma_platform.agents.billing import BillingAgent
from pharma_platform.agents.ceo_master import CEOMasterAgent
from pharma_platform.agents.ethical_sales import EthicalSalesAgent
from pharma_platform.agents.finance import FinanceAgent
from pharma_platform.agents.hr import HRAgent
from pharma_platform.agents.logistics import LogisticsAgent
from pharma_platform.agents.marketing import MarketingAgent
from pharma_platform.agents.pcd_sales import PCDSalesAgent
from pharma_platform.agents.procurement import ProcurementAgent
from pharma_platform.agents.product_launch import ProductLaunchAgent
from pharma_platform.registry.registry import get_agent_registry

logger = logging.getLogger(__name__)


def register_all_agents() -> None:
    """Instantiate and register all 10 platform agents."""
    registry = get_agent_registry()
    registry.clear()

    agents = [
        CEOMasterAgent(),
        EthicalSalesAgent(),
        PCDSalesAgent(),
        ProcurementAgent(),
        BillingAgent(),
        FinanceAgent(),
        LogisticsAgent(),
        MarketingAgent(),
        ProductLaunchAgent(),
        HRAgent(),
    ]

    for agent in agents:
        registry.register(agent)

    logger.info("Successfully registered %d agents in the platform registry.", len(agents))
