import prisma
import prisma.models
from pydantic import BaseModel


class RetrieveQueryResultResponse(BaseModel):
    """
    The model outlining the response structure for a query result retrieval. It includes details about the query, its complexity score, the AI model it was routed to, and the actual response.
    """

    query_id: str
    query_text: str
    complexity_score: float
    routed_to_model: str
    response: str
    latency: float
    cost: float


async def retrieve_query_result(queryId: str) -> RetrieveQueryResultResponse:
    """
    Retrieves the results of processed queries for the user.

    Args:
        queryId (str): The unique identifier of the query for which the result is being retrieved.

    Returns:
        RetrieveQueryResultResponse: The model outlining the response structure for a query result retrieval. It
        includes details about the query, its complexity score, the AI model it was routed to, and the actual response.
    """
    query = await prisma.models.Query.prisma().find_unique(where={"id": queryId})
    if query is None:
        raise ValueError(f"No query found with ID: {queryId}")
    return RetrieveQueryResultResponse(
        query_id=query.id,
        query_text=query.queryText,
        complexity_score=query.complexityScore
        if query.complexityScore is not None
        else 0.0,
        routed_to_model=query.routedToModel if query.routedToModel else "Unknown",
        response=query.response if query.response else "No response available",
        latency=query.latency if query.latency is not None else 0.0,
        cost=query.cost if query.cost is not None else 0.0,
    )
