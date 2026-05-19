from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    func,
)

from app.db.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    country = Column(String(100), nullable=False, index=True)
    job_title = Column(String(150), nullable=False, index=True)
    department = Column(String(150), nullable=False)
    salary = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), nullable=False)
    employment_type = Column(String(50), nullable=False)
    joining_date = Column(Date, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index(
            "ix_employees_country_job_title",
            "country",
            "job_title",
        ),
    )
