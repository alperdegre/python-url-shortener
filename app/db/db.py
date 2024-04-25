from sqlalchemy.orm import DeclarativeBase, relationship
import os
import sqlalchemy
from sqlalchemy.orm import Mapped
from typing import List
from sqlalchemy.orm import mapped_column, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__= "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    urls: Mapped[List["Url"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Url(Base):
    __tablename__= "url"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    short_url: Mapped[str] = mapped_column()
    long_url: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="urls")


# DATABASE_URL = "sqlite:///test.db"
DATABASE_URL = os.getenv("DATABASE_URL", "")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def try_create():
    Base.metadata.create_all(bind=engine)
