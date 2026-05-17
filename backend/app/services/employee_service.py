from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate


def create_employee(db: Session, employee_data: EmployeeCreate) -> Employee:
    existing_employee = (
        db.query(Employee).filter(Employee.email == employee_data.email).first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=400, detail="Employee with this email already exists"
        )

    employee = Employee(
        name=employee_data.name,
        email=employee_data.email,
        department=employee_data.department,
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee
