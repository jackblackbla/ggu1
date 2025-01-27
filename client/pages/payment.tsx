"use client";
// pages/payment.tsx
import React from 'react';
import { loadTossPayments } from '@tosspayments/tosspayments-sdk';

const CLIENT_KEY = process.env.NEXT_PUBLIC_TOSS_CLIENT_KEY || 'test_ck_...';  // 환경변수에서 클라이언트 키 로드
const CUSTOMER_KEY = 'example-user-123'; // 테스트용 고객 키

export default function PaymentPage() {
  /**
   * 자동결제(빌링) 카드 등록 창을 열기
   * - '카드 등록하기' 버튼 클릭 시점을 기준으로 로드 & 호출
   */
  const handleBillingAuth = async () => {
    try {
      // 토스페이먼츠 SDK 로드 → tossPayments 객체 준비
      const tossPayments = await loadTossPayments(CLIENT_KEY);

      // 결제창 인스턴스 (payment) 생성
      const payment = tossPayments.payment({ customerKey: CUSTOMER_KEY });

      // 자동결제(빌링) 인증창 열기
      await payment.requestBillingAuth({
        method: 'CARD', // 자동결제는 카드만 가능
        successUrl: `${process.env.NEXT_PUBLIC_BASE_URL}/success`,
        failUrl: `${process.env.NEXT_PUBLIC_BASE_URL}/fail`,
        customerEmail: 'user@example.com',
        customerName: '홍길동',
      });
      // → 결제창(카드 등록창)이 열리고, 본인인증이 완료되면 successUrl로 이동
    } catch (error) {
      handlePaymentError(error);
      captureException(error);
    }
  };

  return (
    <div style={{ margin: 16 }}>
      <h1>자동결제(빌링) 카드 등록</h1>
      <p>
        <strong>requestBillingAuth()</strong>로 카드 정보를 등록하고,<br />
        <strong>authKey</strong>와 <strong>customerKey</strong>를 받은 뒤에는
        서버에서 빌링키 발급 API를 호출하세요.
      </p>
      <button
        onClick={handleBillingAuth}
        style={{
          padding: '12px 24px',
          fontSize: '1.2rem',
          backgroundColor: '#0070f3',
          color: '#fff',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
        }}
      >
        카드 등록하기
      </button>
    </div>
  );
}