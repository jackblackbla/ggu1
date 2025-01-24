from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/payment", tags=["payment"])

class PaymentInitRequest(BaseModel):
    amount: int

class PaymentInitResponse(BaseModel):
    payment_id: str
    redirectUrl: str  # 필드명 camelCase로 수정
    amount: int
    created_at: datetime

@router.post("/init", response_model=PaymentInitResponse)
async def init_payment(request: PaymentInitRequest):
    """결제 초기화 임시 구현"""
    try:
        return {
            "payment_id": "temp_12345",
            "redirectUrl": "http://localhost:3000/success",  # JSON 키 이름 수정
            "amount": request.amount,
            "created_at": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))