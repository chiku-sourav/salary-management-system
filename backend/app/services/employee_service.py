from fastapi import Depends, HTTPException, status

from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self, repo: EmployeeRepository = Depends()):
        self.repo = repo

    def create(self, employee_data: EmployeeCreate) -> Employee:
        self.__check_employee_email(employee_data)

        return self.repo.create(employee_data)

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
        self.__validate_sorting_fields(sort_by)

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
        return self.__get_employee_by_id(id)

    def update(self, id: int, employee_data: EmployeeUpdate) -> Employee:
        employee = self.__get_employee_by_id(id)

        self.__check_employee_email(employee_data, employee)

        return self.repo.update(employee, employee_data)

    def delete(self, id: int) -> None:
        employee = self.__get_employee_by_id(id)

        self.repo.delete(employee)

    def __get_employee_by_id(self, id: int) -> Employee:

        employee = self.repo.get(id)

        if not employee:
            self.__http_exception(
                status.HTTP_404_NOT_FOUND,
                "Employee not found",
            )

        return employee

    def __check_employee_email(
        self,
        employee_data: EmployeeCreate | EmployeeUpdate,
        employee: Employee | None = None,
    ) -> None:

        if isinstance(employee_data, EmployeeCreate):
            if self.repo.get_by_email(employee_data.email):
                self.__http_exception(
                    status.HTTP_400_BAD_REQUEST,
                    "Employee with this email already exists",
                )
            return

        if isinstance(employee_data, EmployeeUpdate) and employee:
            if (
                employee_data.email
                and employee_data.email != employee.email
                and self.repo.get_by_email(employee_data.email)
            ):
                self.__http_exception(
                    status.HTTP_400_BAD_REQUEST,
                    "Employee with this email already exists",
                )

    def __validate_sorting_fields(self, sort_by: str) -> None:
        valid_sort_fields = {
            "full_name",
            "salary",
            "country",
            "job_title",
            "created_at",
        }

        if sort_by not in valid_sort_fields:
            self.__http_exception(status.HTTP_400_BAD_REQUEST, "Invalid sort_by field")

    def __http_exception(self, status_code: int, detail: str) -> None:
        raise HTTPException(
            status_code=status_code,
            detail=detail,
        )
