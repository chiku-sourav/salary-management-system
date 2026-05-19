from fastapi import APIRouter, Depends, Query, Response, status

from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.schemas.pagination import PaginatedResponse
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(employee: EmployeeCreate, service: EmployeeService = Depends()):
    return service.create(employee)


@router.get(
    "",
    response_model=PaginatedResponse[EmployeeResponse],
    status_code=status.HTTP_200_OK,
)
def get_all(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    country: str | None = Query(default=None),
    job_title: str | None = Query(default=None),
    salary: str | None = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc"),
    service: EmployeeService = Depends(),
):
    return service.get_all(
        page=page,
        page_size=page_size,
        search=search,
        country=country,
        job_title=job_title,
        salary=salary,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get(
    "/{id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
)
def get(id: int, service: EmployeeService = Depends()):
    return service.get(id)


@router.put(
    "/{id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
)
def update(id: int, employee: EmployeeUpdate, service: EmployeeService = Depends()):
    return service.update(id, employee)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(id: int, service: EmployeeService = Depends()):
    service.delete(id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
