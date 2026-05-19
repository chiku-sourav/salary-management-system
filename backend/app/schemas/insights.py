from pydantic import BaseModel


class CountrySalaryInsight(BaseModel):
    country: str
    avg_salary: float
    min_salary: float
    max_salary: float
    employee_count: int


class JobTitleSalaryInsight(BaseModel):
    country: str
    job_title: str
    avg_salary: float
    employee_count: int
