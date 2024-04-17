import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import prisma
import prisma.enums
import project.allocate_query_service
import project.analyze_query_complexity_service
import project.manage_user_accounts_service
import project.monitor_system_health_service
import project.process_query_service
import project.retrieve_query_result_service
import project.submit_feedback_service
import project.submit_query_service
import project.track_financial_metrics_service
import project.view_feedback_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Prompt Router",
    lifespan=lifespan,
    description="The project aims to build an automatic query-routing interface that intelligently routes queries to the most suitable AI model (GPT-4 Turbo, Claude 3 Opus, Gemini 1.5 Pro, or others) based on the query's complexity, the need for efficiency, and cost considerations. The system prioritizes high-quality responses while minimizing latency and keeping within a budget of up to $5,000 per month. Through the user interviews, we've identified the necessity for handling 10K queries per month, with a demand for prompt responses. The choice of model varies with the task: complex NLP tasks will utilise GPT-4 Turbo for its superior understanding and generation capabilities; Claude 3 Opus is preferred for engaging content creation with a focus on moderation and safety; and Gemini 1.5 Pro will serve specific domains requiring up-to-date industry knowledge. Strategies for reducing costs include examining various aspects like accuracy, uniqueness, and information timeliness. Additionally, techniques for lowering latency were discussed, suggesting the use of caching, CDNs, database optimization, and other performance-tuning methods. The technical stack for implementing this solution includes Python for programming, FastAPI for the API framework, PostgreSQL for the database, and Prisma for the ORM. This stack was chosen for its responsiveness, scalability, and developer-friendly nature, which aligns with our goals of creating a fast, reliable, and cost-effective query-routing interface.",
)


@app.post(
    "/query/submit", response_model=project.submit_query_service.SubmitQueryResponse
)
async def api_post_submit_query(
    userId: str, queryText: str
) -> project.submit_query_service.SubmitQueryResponse | Response:
    """
    Allows users to submit queries directly through the web UI.
    """
    try:
        res = await project.submit_query_service.submit_query(userId, queryText)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/query/analyze",
    response_model=project.analyze_query_complexity_service.AnalyzeQueryComplexityResponse,
)
async def api_post_analyze_query_complexity(
    query_text: str, user_id: str
) -> project.analyze_query_complexity_service.AnalyzeQueryComplexityResponse | Response:
    """
    Analyzes the complexity of a user-submitted query and categorizes it accordingly.
    """
    try:
        res = await project.analyze_query_complexity_service.analyze_query_complexity(
            query_text, user_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feedback/submit",
    response_model=project.submit_feedback_service.SubmitFeedbackResponse,
)
async def api_post_submit_feedback(
    userId: Optional[str], content: str, queryId: Optional[str]
) -> project.submit_feedback_service.SubmitFeedbackResponse | Response:
    """
    Endpoint to allow users to submit feedback about the system.
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(
            userId, content, queryId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/query/allocate",
    response_model=project.allocate_query_service.AllocateQueryResponse,
)
async def api_post_allocate_query(
    query_text: str, user_id: str, complexity_score: float, preferred_models: List[str]
) -> project.allocate_query_service.AllocateQueryResponse | Response:
    """
    Allocates a user query to the best-suited AI model based on current performance, cost metrics, and remaining budget.
    """
    try:
        res = await project.allocate_query_service.allocate_query(
            query_text, user_id, complexity_score, preferred_models
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/manage/{userId}",
    response_model=project.manage_user_accounts_service.ManageUserAccountsResponse,
)
async def api_put_manage_user_accounts(
    newRole: prisma.enums.UserRole, userId: str, isActive: Optional[bool]
) -> project.manage_user_accounts_service.ManageUserAccountsResponse | Response:
    """
    Endpoint for admin roles to manage user accounts and roles.
    """
    try:
        res = await project.manage_user_accounts_service.manage_user_accounts(
            newRole, userId, isActive
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/finance/metrics",
    response_model=project.track_financial_metrics_service.FinanceMetricsResponse,
)
async def api_get_track_financial_metrics() -> project.track_financial_metrics_service.FinanceMetricsResponse | Response:
    """
    Allows finance and admin roles to track and report on budget and financial metrics.
    """
    try:
        res = await project.track_financial_metrics_service.track_financial_metrics()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/system/health",
    response_model=project.monitor_system_health_service.SystemHealthResponse,
)
async def api_get_monitor_system_health() -> project.monitor_system_health_service.SystemHealthResponse | Response:
    """
    Provides real-time diagnostics and health reports of the system.
    """
    try:
        res = await project.monitor_system_health_service.monitor_system_health()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/query/process", response_model=project.process_query_service.ProcessQueryResponse
)
async def api_post_process_query(
    queryText: str, userId: str, sessionId: Optional[str]
) -> project.process_query_service.ProcessQueryResponse | Response:
    """
    Processes a user query for complexity analysis and model allocation, ensuring the fastest response time.
    """
    try:
        res = await project.process_query_service.process_query(
            queryText, userId, sessionId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/query/result/{queryId}",
    response_model=project.retrieve_query_result_service.RetrieveQueryResultResponse,
)
async def api_get_retrieve_query_result(
    queryId: str,
) -> project.retrieve_query_result_service.RetrieveQueryResultResponse | Response:
    """
    Retrieves the results of processed queries for the user.
    """
    try:
        res = await project.retrieve_query_result_service.retrieve_query_result(queryId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/feedback/view", response_model=project.view_feedback_service.ViewFeedbackResponse
)
async def api_get_view_feedback() -> project.view_feedback_service.ViewFeedbackResponse | Response:
    """
    Allows admins to view collected feedback for analysis.
    """
    try:
        res = await project.view_feedback_service.view_feedback()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
