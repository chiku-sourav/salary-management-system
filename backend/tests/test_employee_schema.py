from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.employee import EmployeeCreate


def test_create_employee_valid():
    employee = EmployeeCreate(
        full_name="John Doe",
        email="john@example.com",
        country="India",
        job_title="Backend Engineer",
        department="Engineering",
        salary=Decimal("75000.50"),
        currency="INR",
        employment_type="Full-time",
        joining_date="2025-01-10",
    )

    assert employee.full_name == "John Doe"
    assert employee.salary == Decimal("75000.50")


def test_create_employee_invalid_salary():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            full_name="John Doe",
            email="john@example.com",
            country="India",
            job_title="Backend Engineer",
            department="Engineering",
            salary=-5000,
            currency="INR",
            employment_type="Full-time",
            joining_date="2025-01-10",
        )


def test_create_employee_missing_name():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            full_name="",
            email="john@example.com",
            country="India",
            job_title="Backend Engineer",
            department="Engineering",
            salary=50000,
            currency="INR",
            employment_type="Full-time",
            joining_date="2025-01-10",
        )
