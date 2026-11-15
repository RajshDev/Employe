from employee.database import Base
from typing import Optional
import datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, PrimaryKeyConstraint, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column


class TblEmployeeMaster(Base):
    __tablename__ = 'tbl_employee_master'
    __table_args__ = (
        PrimaryKeyConstraint('sno', name='tbl_employee_master_pkey'),
        UniqueConstraint('email_id', name='tbl_employee_master_email_id_key'),
        UniqueConstraint('employee_id', name='tbl_employee_master_employee_id_key')
    )

    sno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(20), nullable=False)
    employee_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_icsr_employee: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    email_id: Mapped[Optional[str]] = mapped_column(String(150))
    phone_number: Mapped[Optional[str]] = mapped_column(String(15))
    gender: Mapped[Optional[bool]] = mapped_column(Boolean)
    date_of_birth: Mapped[Optional[datetime.date]] = mapped_column(Date)
