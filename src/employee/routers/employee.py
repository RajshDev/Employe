from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from employee.database import get_db
from employee.schemas.employee import EmployeeResponse,EmployeeCreate
from employee.services import employee as employee_service

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("", response_model=list[EmployeeResponse])
def list_employees(
    is_icsr_employee: bool | None = None,
    gender: bool | None = None,
    name: str | None = None,
    employee_id: str | None = None,
    db: Session = Depends(get_db),
):
    return employee_service.list_employees(db, is_icsr_employee, gender, name, employee_id)

@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    return employee_service.create_employee(db, data)