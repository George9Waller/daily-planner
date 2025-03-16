from datetime import datetime
from typing import Optional, Literal

from sqlalchemy import DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column

from data import db

PrintJobState = Literal["PENDING", "SENT"]


class PrintJob(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow()
    )
    state: Mapped[PrintJobState] = mapped_column(default="PENDING")
    print_data: Mapped[dict] = mapped_column(JSON())
    errors: Mapped[Optional[dict]] = mapped_column(JSON())
    is_printable: Mapped[bool] = mapped_column(default=True)
