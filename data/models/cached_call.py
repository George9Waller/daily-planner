from datetime import datetime
from typing import Union

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from data import db


class CachedCall(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow()
    )
    function: Mapped[str]
    call_args_kwargs: Mapped[dict] = mapped_column(JSONB())
    result: Mapped[Union[dict, list]] = mapped_column(JSONB())
