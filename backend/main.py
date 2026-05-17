from fastapi import FastAPI

from app.api.employees import router as employee_router

app = FastAPI()

app.include_router(employee_router)
