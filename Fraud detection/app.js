//Front-End Integration (React)
import { useState, useRef, useEffect } from 'react';

function Checkout({ userId, cartTotal }) {
  const [keyData, setKeyData] = useState([]);
  const [mouseData, setMouseData] = useState([]);
  const inputRef = useRef();

  useEffect(() => {
    const el = inputRef.current;
    const onKeyDown = e => setKeyData(d => [...d, {type:'down',key:e.key,time:performance.now()}]);
    const onKeyUp   = e => setKeyData(d => [...d, {type:'up',key:e.key,time:performance.now()}]);
    const onMouseMove = e => setMouseData(m => [...m, {x:e.clientX,y:e.clientY,time:performance.now()}]);

    el.addEventListener('keydown', onKeyDown);
    el.addEventListener('keyup', onKeyUp);
    document.addEventListener('mousemove', onMouseMove);
    return () => {
      el.removeEventListener('keydown', onKeyDown);
      el.removeEventListener('keyup', onKeyUp);
      document.removeEventListener('mousemove', onMouseMove);
    };
  }, []);

  const onPay = async () => {
    const resp = await fetch('/api/pay', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ userId, cartTotal, keyData, mouseData })
    });
    const json = await resp.json();
    if (resp.status === 403) {
      // Show OTP modal
    } else {
      // Proceed to payment success
    }
  };

  return (
    <div>
      <input ref={inputRef} placeholder="Card Number" />
      <button onClick={onPay}>Pay Now</button>
    </div>
  );
}
