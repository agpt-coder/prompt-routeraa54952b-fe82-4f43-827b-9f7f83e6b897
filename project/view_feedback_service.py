from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class FeedbackDetail(BaseModel):
    """
    Detailed information about a single piece of feedback.
    """

    id: str
    created_at: datetime
    content: str
    userId: str
    queryId: Optional[str] = None


class ViewFeedbackResponse(BaseModel):
    """
    Response model containing a list of all feedback submitted by users for admin analysis.
    """

    feedbacks: List[FeedbackDetail]


async def view_feedback() -> ViewFeedbackResponse:
    """
    Allows admins to view collected feedback for analysis.

    This function retrieves all feedback from the database, including details about the user who submitted each feedback
    and any associated query, then structures it into a response model for admin analysis.

    Args:
        None

    Returns:
        ViewFeedbackResponse: Response model containing a list of all feedback submitted by users for admin analysis.

    Example:
        view_feedback()
        > <ViewFeedbackResponse object>  # Contains a populated list of feedback details for analysis
    """
    feedback_records = await prisma.models.Feedback.prisma().find_many(
        include={"user": True, "query": True}
    )
    response_feedbacks = [
        FeedbackDetail(
            id=feedback.id,
            created_at=feedback.createdAt,
            content=feedback.content,
            userId=feedback.userId,
            queryId=feedback.queryId,
        )
        for feedback in feedback_records
    ]
    response = ViewFeedbackResponse(feedbacks=response_feedbacks)
    return response
