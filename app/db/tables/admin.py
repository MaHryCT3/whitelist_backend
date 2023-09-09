from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.declarative import BaseDeclarative, intpk


class Admin(BaseDeclarative):
    __tablename__ = 'admin'

    id: Mapped[intpk]
    vk_id: Mapped[int] = mapped_column(BigInteger, unique=True)
