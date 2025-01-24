from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database
from app.routes import payment

# 데이터베이스 초기화
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="GGU1 Subscription API")
app.include_router(payment.router)

# CORS 설정
origins = [
    "http://localhost:3000",  # React 개발 서버
    "http://localhost:5173",  # Vite 개발 서버
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 테스트용 루트 엔드포인트
@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "GGU1 Subscription API is running"
    }

# 데이터베이스 연결 테스트
@app.get("/db-test")
def test_db(db: Session = Depends(database.get_db)):
    try:
        # 간단한 쿼리 실행
        db.execute("SELECT 1")
        return {"status": "success", "message": "Database connection is working"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 테스트용 사용자 생성 엔드포인트
@app.post("/test/create-user")
def create_test_user(db: Session = Depends(database.get_db)):
    try:
        test_user = models.User(
            username="testuser",
            email="test@example.com",
            password="hashed_password_here",  # 실제로는 해시된 비밀번호를 사용해야 함
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        return {"status": "success", "user_id": test_user.id}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}