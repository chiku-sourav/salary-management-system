from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.employee import Employee


class InsightsRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_country_salary_stats(self):
        return (
            self.db.query(
                Employee.country.label("country"),
                func.avg(Employee.salary).label("avg_salary"),
                func.min(Employee.salary).label("min_salary"),
                func.max(Employee.salary).label("max_salary"),
                func.count(Employee.id).label("employee_count"),
            )
            .group_by(Employee.country)
            .all()
        )
