import os
import random
import sys
import time

from faker import Faker
from sqlalchemy import insert

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.db.session import SessionLocal
from app.models.employee import Employee


def seed_employees(total_records: int = 10000, batch_size: int = 2000):
    fake = Faker()
    db = SessionLocal()

    countries = ["India", "Germany", "US", "UK", "Canada"]
    departments = ["Engineering", "Product", "HR", "Sales", "Marketing"]
    currencies = ["INR", "EUR", "USD", "GBP", "CAD"]
    employment_types = ["Full-Time", "Part-Time", "Contractor"]

    print(f"Generating data structures for {total_records} employees...")

    employee_mappings = []
    for i in range(total_records):
        country = random.choice(countries)
        currency = random.choice(currencies)

        employee_mappings.append(
            {
                "full_name": fake.name(),
                "email": f"worker_{i}_{fake.unique.email()}",
                "country": country,
                "job_title": fake.job(),
                "department": random.choice(departments),
                "salary": round(random.uniform(30000, 180000), 2),
                "currency": currency,
                "employment_type": random.choice(employment_types),
                "joining_date": fake.date_between(start_date="-5y", end_date="today"),
            }
        )

    print("Executing batch database insertion...")
    start_time = time.perf_counter()

    try:
        for offset in range(0, total_records, batch_size):
            batch = employee_mappings[offset : offset + batch_size]

            db.execute(insert(Employee), batch)
            print(f"  Inserted records {offset} to {offset + len(batch)}")

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Critical seeding failure encountered: {e}")
        raise e
    finally:
        db.close()

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Success! Seeding complete in {duration:.4f} seconds.")


if __name__ == "__main__":
    seed_employees()
