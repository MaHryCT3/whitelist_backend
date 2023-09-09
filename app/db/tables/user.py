from sqlalchemy import BigInteger, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.declarative import BaseDeclarative, intpk
from app.db.tables.choices import ApprovalStatusChoices


class User(BaseDeclarative):
    __tablename__ = 'user'

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    steamid: Mapped[str] = mapped_column(unique=True)
    approval_status: Mapped[str] = mapped_column(Enum(ApprovalStatusChoices), default=ApprovalStatusChoices.AWAITING)
    alert_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
