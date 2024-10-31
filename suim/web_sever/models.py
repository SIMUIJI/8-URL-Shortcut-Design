from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text

from database import Base


class Url(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True)
    shortUrl = Column(String, unique=True, nullable=False)
    longUrl = Column(String, unique=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
