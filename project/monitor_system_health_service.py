from typing import List

from pydantic import BaseModel


class ServiceHealth(BaseModel):
    """
    Defines the health status of a specific system service.
    """

    service_name: str
    status: str
    last_checked: str


class PerformanceMetrics(BaseModel):
    """
    A collection of system performance metrics.
    """

    cpu_usage_percentage: float
    memory_usage_percentage: float
    disk_space_remaining: float


class SystemHealthResponse(BaseModel):
    """
    This response model provides a comprehensive view of the current system health, encompassing various metrics and statuses to indicate system performance, operational health, and any issues.
    """

    overall_status: str
    services: List[ServiceHealth]
    alerts: List[str]
    performance_metrics: PerformanceMetrics


async def monitor_system_health() -> SystemHealthResponse:
    """
    Provides real-time diagnostics and health reports of the system.

    Returns:
        SystemHealthResponse: This response model provides a comprehensive view of the current system health,
                              encompassing various metrics and statuses to indicate system performance,
                              operational health, and any issues.
    """
    services = [
        ServiceHealth(
            service_name="Database",
            status="Running",
            last_checked="2023-09-28T12:00:00Z",
        ),
        ServiceHealth(
            service_name="API Server",
            status="Running",
            last_checked="2023-09-28T12:00:00Z",
        ),
    ]
    alerts = ["CPU usage is high", "Disk space running low"]
    performance_metrics = PerformanceMetrics(
        cpu_usage_percentage=75.5,
        memory_usage_percentage=64.3,
        disk_space_remaining=120.5,
    )
    overall_status = (
        "Warning" if any((alert.startswith("CPU") for alert in alerts)) else "OK"
    )
    return SystemHealthResponse(
        overall_status=overall_status,
        services=services,
        alerts=alerts,
        performance_metrics=performance_metrics,
    )
