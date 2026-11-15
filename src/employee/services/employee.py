from sqlalchemy import select
from sqlalchemy.orm import Session
from employee.models import TblEmployeeMaster
from employee.middleware import EmployeeAlreadyExistsError
from employee.schemas.employee import EmployeeCreate
# def list_employees(db: Session) -> list[TblEmployeeMaster]:
#     return list(db.scalars(select(TblEmployeeMaster)).all())

def list_employees(
    db: Session,
    is_icsr_employee: bool | None = None,
    gender: bool | None = None,
    name: str | None = None,
    employee_id: str | None = None,
) -> list[TblEmployeeMaster]:
    stmt = select(TblEmployeeMaster)
    if is_icsr_employee is not None:
        stmt = stmt.where(TblEmployeeMaster.is_icsr_employee == is_icsr_employee)
    if gender is not None:
        stmt = stmt.where(TblEmployeeMaster.gender == gender)
    if name:
        stmt = stmt.where(TblEmployeeMaster.employee_name.ilike(f"%{name}%"))
    if employee_id:
        stmt = stmt.where(TblEmployeeMaster.employee_id == employee_id)
    return list(db.scalars(stmt).all())

def create_employee(db: Session, data: EmployeeCreate) -> TblEmployeeMaster:
    stmt = select(TblEmployeeMaster).where(TblEmployeeMaster.employee_id == data.employee_id)
    if db.scalars(stmt).first():
        raise EmployeeAlreadyExistsError()
    emp = TblEmployeeMaster(**data.model_dump())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp