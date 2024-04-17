from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class AllocateQueryResponse(BaseModel):
    """
    Provides details about the allocated AI model for the query, including expected cost and latency.
    """

    allocated_model: str
    expected_cost: float
    expected_latency: float
    availability: bool


async def allocate_query(
    query_text: str, user_id: str, complexity_score: float, preferred_models: List[str]
) -> AllocateQueryResponse:
    """
    Allocates a user query to the best-suited AI model based on current performance, cost metrics, and remaining budget.

    Args:
        query_text (str): The text of the query to be processed.
        user_id (str): The ID of the user submitting the query for resource tracking and analysis.
        complexity_score (float): A numerical value representing the estimated complexity of the query, used to aid in model allocation.
        preferred_models (List[str]): User's preference for AI models, if any, specified as a list of model names.

    Returns:
        AllocateQueryResponse: Provides details about the allocated AI model for the query, including expected cost and latency.
    """
    ai_models = await prisma.models.AIModel.prisma().find_many()
    if preferred_models:
        ai_models = [model for model in ai_models if model.name in preferred_models]
    suitable_models = sorted(ai_models, key=lambda x: x.costPerQuery)
    if suitable_models:
        selected_model = suitable_models[0]
        response = AllocateQueryResponse(
            allocated_model=selected_model.name,
            expected_cost=selected_model.costPerQuery,
            expected_latency=selected_model.averageLatency,
            availability=True,
        )
        return response
    else:
        raise ValueError("No suitable AI models found.")
