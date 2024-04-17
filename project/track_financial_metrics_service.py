from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class FinanceMetricsResponse(BaseModel):
    """
    Defines the structure of the response containing various financial metrics important for administration and financial oversight. This encapsulates expenditures, budget status, and other relevant financial data to inform strategic financial decisions.
    """

    totalExpenditure: float
    monthlyBudget: float
    remainingBudget: float
    costPerQuery: float
    budgetAlerts: List[str]
    financialHealthScore: float


async def track_financial_metrics() -> FinanceMetricsResponse:
    """
    Allows finance and admin roles to track and report on budget and financial metrics.

    This function computes various key financial metrics such as total expenditure, monthly budget, remaining budget,
    average cost per query, budget alerts if thresholds are exceeded, and an overall financial health score.

    Returns:
        FinanceMetricsResponse: Defines the structure of the response containing various financial metrics important for administration and financial oversight. This encapsulates expenditures, budget status, and other relevant financial data to inform strategic financial decisions.
    """
    monthly_budget = 5000
    budget_alert_threshold = 500
    total_expenditure = sum(
        (
            query.cost
            for query in await prisma.models.Query.prisma().find_many()
            if query.cost
        )
    )
    remaining_budget = monthly_budget - total_expenditure
    total_queries = await prisma.models.Query.prisma().count()
    cost_per_query = total_expenditure / total_queries if total_queries else 0
    budget_alerts = (
        ["Remaining budget is below threshold."]
        if remaining_budget < budget_alert_threshold
        else []
    )
    financial_health_score = (
        remaining_budget / monthly_budget * 100 if monthly_budget else 0
    )
    return FinanceMetricsResponse(
        totalExpenditure=total_expenditure,
        monthlyBudget=monthly_budget,
        remainingBudget=remaining_budget,
        costPerQuery=cost_per_query,
        budgetAlerts=budget_alerts,
        financialHealthScore=financial_health_score,
    )
