from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class SubmitFeedbackResponse(BaseModel):
    """
    Confirmation response upon successful submission of feedback.
    """

    success: bool
    message: str


async def submit_feedback(
    userId: Optional[str], content: str, queryId: Optional[str]
) -> SubmitFeedbackResponse:
    """
    Endpoint to allow users to submit feedback about the system.

    Args:
        userId (Optional[str]): The unique identifier of the user submitting the feedback. Optional for allowing anonymous feedback.
        content (str): Detailed feedback provided by the user. This can include both positive and negative experiences, suggestions for improvement, or general comments about the system.
        queryId (Optional[str]): Optional field to associate the feedback with a specific query the user had submitted earlier. Useful for contextual feedback on query performance or results.

    Returns:
        SubmitFeedbackResponse: Confirmation response upon successful submission of feedback.

    Example:
        await submit_feedback(userId="12345", content="Great Service!", queryId="98765")
        > SubmitFeedbackResponse(success=True, message="Thank you for your feedback!")
    """
    feedback_creation = await prisma.models.Feedback.prisma().create(
        data={
            "userId": userId if userId else None,
            "content": content,
            "queryId": queryId if queryId else None,
        }
    )
    if feedback_creation:
        return SubmitFeedbackResponse(
            success=True, message="Thank you for your feedback!"
        )
    else:
        return SubmitFeedbackResponse(
            success=False, message="Failed to submit feedback."
        )
