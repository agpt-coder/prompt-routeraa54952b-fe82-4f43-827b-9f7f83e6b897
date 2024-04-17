import prisma
import prisma.models
from pydantic import BaseModel


class SubmitQueryResponse(BaseModel):
    """
    This model provides feedback to the user about the successful reception of their query.
    """

    queryId: str
    message: str = "Query successfully submitted. Track it with the provided ID."


async def submit_query(userId: str, queryText: str) -> SubmitQueryResponse:
    """
    Allows users to submit queries directly through the web UI.

    Args:
        userId (str): The unique identifier of the user submitting the query.
        queryText (str): The actual text of the query that the user wants to submit.

    Returns:
        SubmitQueryResponse: This model provides feedback to the user about the successful reception of their query including a unique queryId and a confirmation message.

    Example:
        asyncio.run(submit_query("example-user-id", "What is the current stock price of XYZ corporation?"))
        > SubmitQueryResponse(queryId="generated-query-id", message="Query successfully submitted. Track it with the provided ID.")
    """
    query = await prisma.models.Query.prisma().create(
        data={"queryText": queryText, "userId": userId}
    )
    return SubmitQueryResponse(
        queryId=query.id,
        message="Query successfully submitted. Track it with the provided ID.",
    )
