from .Base import Base
from sqlalchemy import String, UniqueConstraint, PrimaryKeyConstraint, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[int] = mapped_column(Integer, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    start_location: Mapped[str] = mapped_column(String, nullable=False)
    end_location: Mapped[str] = mapped_column(String, nullable=False)
    available_tickets: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('route_id', name='pk_route'),
    )