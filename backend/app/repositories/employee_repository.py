from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(
        self,
        page: int,
        page_size: int,
        search: str | None,
        country: str | None,
        job_title: str | None,
        salary: str | None,
        sort_by: str,
        sort_order: str,
    ) -> tuple[list[Employee], int]:
        stmt = select(Employee)

        if search:
            stmt = stmt.where(
                or_(
                    Employee.full_name.ilike(f"%{search}%"),
                    Employee.email.ilike(f"%{search}%"),
                    Employee.department.ilike(f"%{search}%"),
                    Employee.job_title.ilike(f"%{search}%"),
                )
            )

        if country:
            stmt = stmt.where(Employee.country == country)
        if job_title:
            stmt = stmt.where(Employee.job_title == job_title)
        if salary:
            stmt = stmt.where(Employee.salary == salary)

        sortable_fields = {
            "full_name": Employee.full_name,
            "salary": Employee.salary,
            "country": Employee.country,
            "job_title": Employee.job_title,
            "created_at": Employee.created_at,
        }
        sort_column = sortable_fields.get(sort_by, Employee.created_at)
        stmt = stmt.order_by(
            asc(sort_column) if sort_order == "asc" else desc(sort_column)
        )

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.scalar(count_stmt) or 0

        offset = (page - 1) * page_size
        stmt = stmt.offset(offset).limit(page_size)
        items = list(self.db.scalars(stmt).all())

        return items, total

    def get(self, id: int) -> Employee | None:
        return self.db.get(Employee, id)

    def get_by_email(self, email: EmailStr) -> Employee | None:
        return self.db.scalar(select(Employee).filter_by(email=email))

    def create(self, data: EmployeeCreate) -> Employee:
        employee = Employee(**data.model_dump())

        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)

        return employee

    def update(self, employee: Employee, data: EmployeeUpdate) -> Employee:

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(employee, key, value)

        self.db.commit()
        self.db.refresh(employee)

        return employee

    def delete(self, employee: Employee) -> None:
        self.db.delete(employee)
        self.db.commit()

        return None
