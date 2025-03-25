from datetime import datetime, timezone
from typing import Literal, Optional

from sqlalchemy import JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from data import db

PrintJobState = Literal["PENDING", "SENT"]


class PrintJob(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    state: Mapped[PrintJobState] = mapped_column(default="PENDING")
    print_data: Mapped[dict] = mapped_column(JSON())
    errors: Mapped[Optional[dict]] = mapped_column(JSON())
    is_printable: Mapped[bool] = mapped_column(default=True)
