import os
import pathlib
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

def _load_env():
    root_env = pathlib.Path(__file__).resolve().parents[3] / ".env"
    backend_env = pathlib.Path(__file__).resolve().parents[2] / ".env"
    for p in (root_env, backend_env):
        if p.exists():
            for line in p.read_text().splitlines():
                s = line.strip()
                if not s or s.startswith("#") or "=" not in s:
                    continue
                k, v = s.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

_load_env()

DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql+psycopg2://influnce:influnce_password@localhost:5432/influnce_ai"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    access_token = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    expires_in = Column(Integer)
