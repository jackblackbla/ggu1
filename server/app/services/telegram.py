import os
import requests
from typing import Optional
from fastapi import HTTPException

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_link(telegram_id: str, link_url: str) -> bool:
    """텔레그램 사용자에게 링크 메시지 전송"""
    if not TELEGRAM_TOKEN:
        raise HTTPException(status_code=500, detail="Telegram token not configured")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": telegram_id,
        "text": f"🔔 구독해 주셔서 감사합니다!\n이번 달 멤버십 방 입장 링크: {link_url}"
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Telegram API error: {response.text}"
        )
    return True