# app/routes/payment.py

import os
import base64
import requests
import httpx
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Subscription
# 필요하다면 from app.models import TelegramLink
# 필요하다면 from app.services.telegram import send_link

# ---------------------------
# 1) APIRouter 단일 선언
# ---------------------------
router = APIRouter(prefix="/payment", tags=["payment"])


# ---------------------------
# 2) Toss Auth Header 헬퍼
# ---------------------------
def toss_auth_header():
    """
    토스페이먼츠 Basic Auth 헤더 생성
    (secretKey + ':' 를 Base64로 인코딩)
    """
    secret_key = os.getenv("TOSS_SECRET_KEY")
    if not secret_key:
        raise HTTPException(
            status_code=500,
            detail="TOSS_SECRET_KEY not configured in environment"
        )
    encoded = base64.b64encode(f"{secret_key}:".encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }


# ---------------------------
# 3) /payment/billing : 빌링키 발급
# ---------------------------
class BillingRequest(BaseModel):
    authKey: str
    customerKey: str

@router.post("/billing")
async def process_billing(request: BillingRequest):
    """토스페이먼츠: 자동결제(빌링) 인증 성공 후, 빌링키 발급 API 호출"""
    try:
        # 1) 시크릿 키 가져오기
        secret_key = os.getenv('TOSS_SECRET_KEY')
        if not secret_key:
            print("TOSS_SECRET_KEY not found or empty")
            raise HTTPException(status_code=500, detail="TOSS_SECRET_KEY not configured")

        # 2) Base64 인코딩 (secretKey + :)
        raw_value = f"{secret_key}:"
        encoded_value = base64.b64encode(raw_value.encode("utf-8")).decode("utf-8")
        auth_header = f"Basic {encoded_value}"

        async with httpx.AsyncClient() as client:
            print(f"TOSS_SECRET_KEY (raw): {secret_key}")
            response = await client.post(
                "https://api.tosspayments.com/v1/billing/authorizations/issue",
                json={
                    "authKey": request.authKey,
                    "customerKey": request.customerKey
                },
                headers={
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
            )
            print("Response text:", response.text)
            response.raise_for_status()
            return response.json()  # 여기서 billingKey 등 응답

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Toss API error: {e.response.text}"
        )

# ---------------------------
# 4) /payment/init : 일반 결제 초기화
# ---------------------------
class PaymentInitRequest(BaseModel):
    amount: int
    orderId: str
    orderName: str
    successUrl: str
    failUrl: str

class PaymentInitResponse(BaseModel):
    checkoutUrl: str
    paymentKey: str
    orderId: str
    amount: int
    currency: str = "KRW"
    requestedAt: str  # ISO8601 형식
    status: str       # 결제 상태

@router.post("/init", response_model=PaymentInitResponse)
async def init_payment(request: PaymentInitRequest):
    """
    토스페이먼츠 일반 결제창 초기화 API:
      1) request.amount, request.orderId 등으로 결제 생성
      2) checkoutUrl를 반환 → 클라이언트에서 결제창으로 이동
    """
    try:
        print(f"TOSS_SECRET_KEY: {os.getenv('TOSS_SECRET_KEY', 'NOT_FOUND')}")
        headers = toss_auth_header()
        payload = {
            "amount": request.amount,
            "orderId": request.orderId,
            "orderName": request.orderName,
            "successUrl": request.successUrl,
            "failUrl": request.failUrl,
            "currency": "KRW",
            "method": "카드"
        }

        # requests (동기) 사용. httpx.AsyncClient()도 가능
        response = requests.post(
            "https://api.tosspayments.com/v1/payments",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        payment_data = response.json()

        return {
            "checkoutUrl": payment_data["checkoutUrl"],
            "paymentKey": payment_data["paymentKey"],
            "orderId": request.orderId,
            "amount": request.amount,
            "requestedAt": datetime.now().isoformat(),
            "status": payment_data["status"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# 5) /payment/test-webhook : 테스트용 시뮬레이션
# ---------------------------
@router.post("/test-webhook")
async def mock_payment_webhook(db: Session = Depends(get_db)):
    """
    결제 웹훅 시뮬레이션:
      - 현재 날짜 기반으로 month_key 산출
      - DB에 Subscription 레코드 삽입 (user_id=999 등)
    """
    try:
        today = datetime.now()
        test_day = os.getenv('TEST_MODE_DAY')
        if test_day and test_day.isdigit():
            current_day = int(test_day)
        else:
            current_day = today.day

        if current_day <= 15:
            month_key = today.strftime("%Y-%m")
            link_sent = True
        else:
            next_month = today.replace(day=28) + timedelta(days=4)
            month_key = next_month.strftime("%Y-%m")
            link_sent = False

        new_sub = Subscription(
            user_id=999,  # 예시
            month_key=month_key,
            link_sent=link_sent,
            payment_date=datetime.now()
        )
        db.add(new_sub)
        db.commit()

        return {
            "message": f"테스트 완료: month_key={month_key}, link_sent={link_sent}"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))