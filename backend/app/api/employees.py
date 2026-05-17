from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from app.services.employee_service import create_employee

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee_api(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db, employee)
