from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from employee.database import get_db
from employee.schemas.employee import EmployeeResponse
from employee.services import employee as employee_service

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return employee_service.list_employees(db)