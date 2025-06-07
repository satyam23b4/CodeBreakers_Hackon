const keyEvents = [];
const mouseEvents = [];
const input = document.getElementById('card');

// Capture keystrokes
input.addEventListener('keydown', e =>
  keyEvents.push({key:e.key,type:'down',time:performance.now()}));
input.addEventListener('keyup',   e =>
  keyEvents.push({key:e.key,type:'up',  time:performance.now()}));

// Capture mouse moves
document.addEventListener('mousemove', e =>
  mouseEvents.push({x:e.clientX, y:e.clientY, time:performance.now()}));

// On Pay Now
document.getElementById('payBtn').onclick = async () => {
  const resp = await fetch('/predict', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ keyEvents, mouseEvents })
  });
  const {probability, label} = await resp.json();
  const div = document.getElementById('result');
  if (label==='Fraudulent') {
    div.innerHTML = `<span class="flag">⚠️ Fraud Suspected (${probability})</span>`;
  } else {
    div.innerHTML = `<span class="ok">✅ Genuine Transaction (${probability})</span>`;
  }
};
