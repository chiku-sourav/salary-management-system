from datetime import date

from fastapi.testclient import TestClient

from app.models.employee import Employee


def test_country_salary_insights_returns_empty_list_when_no_employees(
    client: TestClient,
):
    response = client.get("/insights/country-salary")

    assert response.status_code == 200
    assert response.json() == []


def test_country_salary_insights_returns_correct_stats(
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
            country="USA",
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

    response = client.get("/insights/country-salary")

    assert response.status_code == 200

    data = response.json()

    india = next(x for x in data if x["country"] == "India")

    assert india["avg_salary"] == 2000
    assert india["min_salary"] == 1000
    assert india["max_salary"] == 3000
    assert india["employee_count"] == 2


def test_country_salary_insights_groups_by_country(
    client: TestClient,
    db_session,
):
    employees = [
        Employee(
            full_name="D",
            email="d@test.com",
            country="India",
            job_title="Engineer",
            salary=1000,
            department="Engineering",
            currency="EUR",
            employment_type="Full-Time",
            joining_date=date.today(),
        ),
        Employee(
            full_name="E",
            email="e@test.com",
            country="USA",
            job_title="Engineer",
            salary=5000,
            department="Engineering",
            currency="EUR",
            employment_type="Full-Time",
            joining_date=date.today(),
        ),
    ]

    db_session.add_all(employees)
    db_session.commit()

    response = client.get("/insights/country-salary")

    data = response.json()

    assert len(data) == 2
