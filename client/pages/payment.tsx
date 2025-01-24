import instance from '../utils/axios';

const handleSubscribe = async () => {
  try {
    console.log('결제 초기화 요청 시작');
    const res = await instance.post('/payment/init', { amount: 9900 });
    console.log('백엔드 응답:', res.data);
    
    if (res.data.redirectUrl) {
      console.log('리다이렉트 URL로 이동:', res.data.redirectUrl);
      window.location.href = res.data.redirectUrl;
    }
  } catch (error) {
    console.error('결제 초기화 실패:', error);
    alert('결제 처리 중 오류가 발생했습니다. 다시 시도해 주세요.');
  }
};

export default function PaymentPage() {
  return (
    <div>
      <h1>결제 페이지</h1>
      <button 
        onClick={handleSubscribe}
        style={{ 
          padding: '12px 24px',
          fontSize: '1.2rem',
          backgroundColor: '#0070f3',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer'
        }}
      >
        구독하기
      </button>
    </div>
  );
}