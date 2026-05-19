from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.employee_controller import router as employee_router
from app.controllers.insights_controller import router as insights_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allows custom headers (like Authorization tokens)
)

app.include_router(employee_router)
app.include_router(insights_router)
