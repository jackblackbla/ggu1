export default function SuccessPage() {
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