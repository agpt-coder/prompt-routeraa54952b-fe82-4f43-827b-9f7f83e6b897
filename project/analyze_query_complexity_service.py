import prisma
import prisma.models
from pydantic import BaseModel


class AnalyzeQueryComplexityResponse(BaseModel):
    """
    Outputs the complexity score of the analyzed query, categorizing it accordingly for further processing.
    """

    complexity_score: float
    complexity_category: str


async def analyze_query_complexity(
    query_text: str, user_id: str
) -> AnalyzeQueryComplexityResponse:
    """
    Analyzes the complexity of a user-submitted query and categorizes it accordingly.

    Args:
        query_text (str): The text of the user's query to analyze.
        user_id (str): The ID of the user submitting the query. This is essential for tracking and learning purposes.

    Returns:
        AnalyzeQueryComplexityResponse: Outputs the complexity score of the analyzed query,
        categorizing it accordingly for further processing.
    """
    complexity_score = calculate_complexity_score(query_text)
    complexity_category = categorize_score(complexity_score)
    await prisma.models.Query.prisma().create(
        data={
            "queryText": query_text,
            "complexityScore": complexity_score,
            "userId": user_id,
        }
    )
    return AnalyzeQueryComplexityResponse(
        complexity_score=complexity_score, complexity_category=complexity_category
    )


def calculate_complexity_score(query_text: str) -> float:
    """
    Calculates the complexity score of a query.

    This is a placeholder function to simulate the complexity analysis.
    In a real scenario, this could be a more sophisticated analysis based
    on various factors like query length, use of specific keywords, etc.

    Args:
        query_text (str): The text of the query to analyze.

    Returns:
        float: A calculated complexity score for the query.
    """
    score = len(query_text) / 100.0
    return score


def categorize_score(score: float) -> str:
    """
    Categorizes the complexity score into 'Low', 'Medium', or 'High'.

    Args:
        score (float): The computed complexity score for a query.

    Returns:
        str: The category of the complexity ('Low', 'Medium', 'High').
    """
    if score < 1.0:
        return "Low"
    elif score < 2.0:
        return "Medium"
    else:
        return "High"
