from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column
from typing_extensions import Annotated

intpk = Annotated[int, mapped_column(primary_key=True, init=False)]


class BaseDeclarative(MappedAsDataclass, DeclarativeBase):
    ...
