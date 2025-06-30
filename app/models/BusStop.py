from .Base import Base
from sqlalchemy import String, UniqueConstraint, PrimaryKeyConstraint, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4


class BusStop(Base):
    __tablename__ = "bus_stops"

    stop_id: Mapped[int] = mapped_column(Integer, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    route_id: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('stop_id', name='pk_bus_stop'),
        UniqueConstraint('name', name='uq_bus_stop_name'),
        UniqueConstraint('route_id', name='uq_bus_stop_route_id'),
    )
