from fastapi import Depends

from app.repositories.insights_repository import InsightsRepository


class InsightsService:
    def __init__(self, repo: InsightsRepository = Depends()):
        self.repo = repo

    def fetch_country_salary_insights(self) -> list:
        results = self.repo.get_country_salary_stats()

        return [
            {
                "country": row.country,
                "avg_salary": round(float(row.avg_salary), 2),
                "min_salary": float(row.min_salary),
                "max_salary": float(row.max_salary),
                "employee_count": row.employee_count,
            }
            for row in results
        ]
