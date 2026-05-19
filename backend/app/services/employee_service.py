from fastapi import Depends, HTTPException, status

from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self, repo: EmployeeRepository = Depends()):
        self.repo = repo

    def create(self, data: EmployeeCreate) -> Employee:
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee with this email already exists",
            )

        employee: Employee = self.repo.create(data)

        return employee

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
    ) -> dict:
        valid_sort_fields = {
            "full_name",
            "salary",
            "country",
            "job_title",
            "created_at",
        }
        if sort_by not in valid_sort_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sort_by field",
            )

        items, total = self.repo.get_all(
            page=page,
            page_size=page_size,
            search=search,
            country=country,
            job_title=job_title,
            salary=salary,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def get(self, id: int) -> Employee:
        return self.repo.get(id)

    def update(self, id: int, data: EmployeeUpdate) -> Employee:
        employee = self.repo.get(id)

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
            )

        if (
            data.email
            and data.email != employee.email
            and self.repo.get_by_email(data.email)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee with this email already exists",
            )

        employee: Employee = self.repo.update(employee, data)

        return employee

    def delete(self, id: int) -> None:
        employee = self.repo.get(id)

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
            )

        self.repo.delete(employee)
