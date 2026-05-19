from datetime import date

from fastapi import status
from fastapi.testclient import TestClient


def test_create_employee_duplicate_email_throws_400(client: TestClient):
    __create_employee(client, index=50)

    payload = {
        "full_name": "Clone Employee",
        "email": "employee50_50@example.com",
        "country": "India",
        "job_title": "Backend Engineer",
        "department": "Engineering",
        "salary": 120000,
        "currency": "INR",
        "employment_type": "Full-Time",
        "joining_date": str(date.today()),
    }

    response = client.post("/employees", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


def test_list_employees_with_pagination(client: TestClient):
    for index in range(15):
        __create_employee(client, index)

    response = client.get("/employees?page=1&page_size=10")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total"] >= 15

    assert len(data["items"]) == 10


def test_search_employees(client: TestClient):
    __create_employee(client, 999)

    response = client.get("/employees?search=Employee 999")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data["items"]) >= 1


def test_sort_employees_by_salary(client: TestClient):
    response = client.get("/employees?sort_by=salary&sort_order=asc")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    print(data)
    salaries = [float(employee["salary"]) for employee in data["items"]]

    assert salaries == sorted(salaries)


def test_update_employee_success(client: TestClient):
    employee = __create_employee(client, index=100)
    employee_id = employee["id"]

    update_payload = {
        "full_name": "Updated Name",
        "email": "updated_email@example.com",
        "country": "Germany",
        "job_title": "Lead Engineer",
        "department": "Engineering",
        "salary": 120000,
        "currency": "EUR",
        "employment_type": "Full-Time",
        "joining_date": employee["joining_date"],
    }

    response = client.put(f"/employees/{employee_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK

    updated_data = response.json()
    assert updated_data["id"] == employee_id
    assert updated_data["full_name"] == "Updated Name"
    assert updated_data["country"] == "Germany"
    assert float(updated_data["salary"]) == 120000


def test_update_non_existent_employee(client: TestClient):
    update_payload = {
        "full_name": "Ghost Employee",
        "email": "ghost@example.com",
        "country": "India",
        "job_title": "Backend Engineer",
        "department": "Engineering",
        "salary": 100000,
        "currency": "INR",
        "employment_type": "Full-Time",
        "joining_date": str(date.today()),
    }

    response = client.put("/employees/99999", json=update_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_employee_success(client: TestClient):
    employee = __create_employee(client, index=200)
    employee_id = employee["id"]

    delete_response = client.delete(f"/employees/{employee_id}")
    assert delete_response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_204_NO_CONTENT,
    ]

    list_response = client.get("/employees?page=1&page_size=10")
    list_data = list_response.json()

    assert not any(emp["id"] == employee_id for emp in list_data["items"])


def test_delete_non_existent_employee(client: TestClient):
    response = client.delete("/employees/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def __create_employee(client: TestClient, index: int) -> dict:
    payload = {
        "full_name": f"Employee {index}",
        "email": f"employee{index}_{index}@example.com",
        "country": "India",
        "job_title": "Backend Engineer",
        "department": "Engineering",
        "salary": 100000 + index,
        "currency": "INR",
        "employment_type": "Full-Time",
        "joining_date": str(date.today()),
    }

    response = client.post("/employees", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    return response.json()
