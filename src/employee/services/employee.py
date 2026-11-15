from sqlalchemy import select
from sqlalchemy.orm import Session
from employee.models import TblEmployeeMaster

def list_employees(db: Session) -> list[TblEmployeeMaster]:
    return list(db.scalars(select(TblEmployeeMaster)).all())

# def get_employee(db: Session, employee_id: str) -> TblEmployeeMaster | None:
#     stmt = select(TblEmployeeMaster).where(TblEmployeeMaster.employee_id == employee_id)
#     return db.scalars(stmt).first()