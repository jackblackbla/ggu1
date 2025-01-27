import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import axios from '../utils/axios';

export default function SuccessPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const processPayment = async () => {
      try {
        const { customerKey, authKey } = router.query;
        
        if (!customerKey || !authKey) {
          throw new Error('결제 정보가 올바르지 않습니다.');
        }

        // 백엔드 API 호출
        await axios.post('/payment/billing', {
          customerKey,
          authKey
        });

        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    processPayment();
  }, [router.query]);

  if (loading) {
    return (
      <div style={{
        textAlign: 'center',
        padding: '40px 20px',
        maxWidth: '600px',
        margin: '0 auto'
      }}>
        <h1 style={{ color: '#4CAF50', marginBottom: '24px' }}>결제 처리 중...</h1>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        textAlign: 'center',
        padding: '40px 20px',
        maxWidth: '600px',
        margin: '0 auto'
      }}>
        <h1 style={{ color: '#f44336', marginBottom: '24px' }}>오류 발생</h1>
        <p style={{ fontSize: '1.1rem', lineHeight: '1.6' }}>
          {error}
        </p>
      </div>
    );
  }

  return (
    <div style={{
      textAlign: 'center',
      padding: '40px 20px',
      maxWidth: '600px',
      margin: '0 auto'
    }}>
      <h1 style={{ color: '#4CAF50', marginBottom: '24px' }}>결제 성공!</h1>
      <p style={{ fontSize: '1.1rem', lineHeight: '1.6' }}>
        구독이 정상적으로 완료되었습니다.
        <br />
        이용해 주셔서 감사합니다.
      </p>
    </div>
  );
}