from datetime import date
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field, field_validator


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


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str

    class Config:
        from_attributes = True
