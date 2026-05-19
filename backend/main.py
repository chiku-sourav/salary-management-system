from fastapi import FastAPI

from app.controllers.employee_controller import router as employee_router

app = FastAPI()

app.include_router(employee_router)
