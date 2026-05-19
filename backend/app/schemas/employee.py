from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    country: str
    job_title: str
    department: str
    salary: Decimal = Field(gt=0)
    currency: str
    employment_type: str
    joining_date: date

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str):
        if not value.strip():
            raise ValueError("full name cannot be empty")
        return value


class EmployeeUpdate(BaseModel):
    full_name: str | None
    email: EmailStr | None
    country: str | None
    job_title: str | None
    department: str | None
    salary: Decimal | None = Field(default=None, gt=0)
    currency: str | None
    employment_type: str | None
    joining_date: date | None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    country: str
    job_title: str
    department: str
    salary: Decimal = Field(gt=0)
    currency: str
    employment_type: str
    joining_date: date
