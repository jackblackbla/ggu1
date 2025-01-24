from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL 형식: mysql+pymysql://username:password@host:port/database_name
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost:3306/ggu1")

# 엔진 설정
engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL 로깅
    pool_size=5,  # 커넥션 풀 크기
    max_overflow=10,  # 최대 초과 커넥션
    pool_timeout=30,  # 커넥션 타임아웃 (초)
)

# 세션 설정
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Base 클래스 정의
Base = declarative_base()

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()