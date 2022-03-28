from fastapi import APIRouter
import requests

department_router = APIRouter()


@department_router.get("/")
def get_department_overview() -> dict:
    return requests.get(f"http://medical_dal:8050/medical_dal/department").json()
