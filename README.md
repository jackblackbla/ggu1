# GGU1 프로젝트 개발자 가이드

## 프로젝트 개요
- **기술 스택**
  - 백엔드: Python FastAPI + SQLAlchemy + MySQL
  - 프론트엔드: React + Axios + React Query
  - 결제 연동: 토스페이먼츠 테스트 모드
  - 커뮤니티: 텔레그램 봇 API

## 초기 설정
```bash
# 백엔드
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 프론트엔드 
cd ../client
npm install
```

## 환경변수 설정 (server/.env)
```ini
DB_HOST=localhost
DB_USER=root
DB_PASS=your_password
DB_NAME=ggu1_db
TOSS_API_KEY=test_sk_xxxx
TELEGRAM_BOT_TOKEN=xxxx:xxxx
```

## 주요 기능 구현 가이드

### 결제 모듈 (server/app/routes/payment.py)
```python
from fastapi import APIRouter, Depends
from app.schemas import PaymentInitRequest
from app.services.payment import process_payment

router = APIRouter(prefix="/payment", tags=["payment"])

@router.post("/init")
async def init_payment(
    request: PaymentInitRequest, 
    db=Depends(get_db)
):
    return await process_payment(request, db)
```

### 텔레그램 서비스 (server/app/services/telegram.py)
```python
import requests

def send_telegram_message(chat_id: str, text: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    return requests.post(url, json=payload)
```

### 스케줄러 설정 (server/app/main.py)
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.subscription import check_expired_subscriptions

scheduler = AsyncIOScheduler()
scheduler.add_job(check_expired_subscriptions, 'cron', hour=0)
scheduler.start()
```

## 실행 방법
```bash
# 백엔드 개발 모드
uvicorn app.main:app --reload --port 8000

# 프론트엔드 개발 모드
cd client && npm start