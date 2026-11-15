from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sno: int
    employee_id: str
    employee_name: str
    email_id: str | None
    phone_number: str | None
    gender: bool | None
    is_icsr_employee: bool
    date_of_birth: date | None
    created_at: datetime
    updated_at: datetime