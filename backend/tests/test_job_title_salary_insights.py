from datetime import date

from fastapi.testclient import TestClient

from app.models.employee import Employee


def test_job_title_salary_insights_groups_by_country_and_job_title(
    client: TestClient,
    db_session,
):
    employees = [
        Employee(
            full_name="A",
            email="a@test.com",
            country="India",
            job_title="Engineer",
            salary=1000,
            department="Engineering",
            currency="EUR",
            employment_type="Full-Time",
            joining_date=date.today(),
        ),
        Employee(
            full_name="B",
            email="b@test.com",
            country="India",
            job_title="Engineer",
            salary=3000,
            department="Engineering",
            currency="EUR",
            employment_type="Full-Time",
            joining_date=date.today(),
        ),
        Employee(
            full_name="C",
            email="c@test.com",
            country="India",
            job_title="Manager",
            salary=5000,
            department="Engineering",
            currency="EUR",
            employment_type="Full-Time",
            joining_date=date.today(),
        ),
    ]

    db_session.add_all(employees)
    db_session.commit()

    response = client.get("/insights/job-title-salary")

    assert response.status_code == 200

    data = response.json()

    engineer = next(
        x for x in data if x["country"] == "India" and x["job_title"] == "Engineer"
    )

    assert engineer["avg_salary"] == 2000
    assert engineer["employee_count"] == 2


def test_salary_values_are_serializable(
    client: TestClient,
    db_session,
):
    employee = Employee(
        full_name="A",
        email="a@test.com",
        country="India",
        job_title="Engineer",
        salary=1234.56,
        department="Engineering",
        currency="EUR",
        employment_type="Full-Time",
        joining_date=date.today(),
    )

    db_session.add(employee)
    db_session.commit()

    response = client.get("/insights/country-salary")

    data = response.json()

    assert isinstance(data[0]["avg_salary"], float)


def test_country_salary_insights_handles_large_dataset(
    client: TestClient,
    db_session,
):
    employees = [
        Employee(
            full_name=f"User {i}",
            email=f"user{i}@test.com",
            country="India",
            job_title="Engineer",
            salary=1000 + i,
            department="Engineering",
            currency="EUR",
            employment_type="Full-Time",
            joining_date=date.today(),
        )
        for i in range(1000)
    ]

    db_session.bulk_save_objects(employees)
    db_session.commit()

    response = client.get("/insights/country-salary")

    assert response.status_code == 200
