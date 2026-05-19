from fastapi import APIRouter, Depends

from app.schemas.insights import (
    CountrySalaryInsight,
    JobTitleSalaryInsight,
)
from app.services.insights_service import InsightsService

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get(
    "/country-salary",
    response_model=list[CountrySalaryInsight],
)
def get_country_salary_insights(service: InsightsService = Depends()):
    return service.fetch_country_salary_insights()
