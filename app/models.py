from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.database import Base


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    visit_duration_minutes = Column(Integer, nullable=False)
    open_hour = Column(String, nullable=True)
    close_hour = Column(String, nullable=True)


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    discovered_places = Column(JSON, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)