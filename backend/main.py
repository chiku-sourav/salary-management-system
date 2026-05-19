from fastapi import FastAPI

from app.controllers.employee_controller import router as employee_router
from app.controllers.insights_controller import router as insights_router

app = FastAPI()

app.include_router(employee_router)
app.include_router(insights_router)
