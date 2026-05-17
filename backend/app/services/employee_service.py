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
        full_name=employee_data.full_name,
        email=employee_data.email,
        department=employee_data.department,
        country=employee_data.country,
        job_title=employee_data.job_title,
        salary=employee_data.salary,
        currency=employee_data.currency,
        employment_type=employee_data.employment_type,
        joining_date=employee_data.joining_date,
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee
