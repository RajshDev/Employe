from datetime import date, datetime
from pydantic import BaseModel, ConfigDict,EmailStr,Field

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

class EmployeeCreate(BaseModel):
    employee_id: str = Field(min_length=3, max_length=20, pattern=r"^ICSR\d{3,}$")
    employee_name: str = Field(min_length=2, max_length=100)
    email_id: EmailStr | None = None
    phone_number: str | None = Field(default=None, pattern=r"^[6-9]\d{9}$")
    gender: bool | None = None
    is_icsr_employee: bool = True
    date_of_birth: date | None = None