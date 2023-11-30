import datetime
import enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, String
from sqlalchemy.dialects.postgresql import ARRAY

from .settings import Base


class Role(str, enum.Enum):
    super_user = 'super_user'
    admin = 'admin'
    user = 'user'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[list[Role]] = mapped_column(ARRAY(String))
    hashed_password: Mapped[str]
    refresh_token: Mapped[str | None]
    create_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    update_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow)
    