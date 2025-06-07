const checkBtn = document.getElementById('checkBtn');
const alertsDiv = document.getElementById('alerts');
const cardAdDiv = document.getElementById('cardAd');
const chartCtx = document.getElementById('chart').getContext('2d');
let chart; // Chart.js instance

checkBtn.onclick = async () => {
  // Gather budgets
  const budgets = {
    Electronics: +document.getElementById('b-electronics').value,
    Groceries:   +document.getElementById('b-groceries').value,
    Fashion:     +document.getElementById('b-fashion').value,
    Other:       +document.getElementById('b-other').value,
  };
  // Gather cart
  const cartItems = [
    {category:'Electronics', amount:+document.getElementById('c-electronics').value},
    {category:'Groceries',  amount:+document.getElementById('c-groceries').value},
    {category:'Fashion',    amount:+document.getElementById('c-fashion').value},
    {category:'Other',      amount:+document.getElementById('c-other').value},
  ];

  // Call backend
  const resp = await fetch('/api/budget/status', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({budgets, cartItems})
  });
  const {status, cardOffer} = await resp.json();

  // Show alerts and prepare chart data
  alertsDiv.innerHTML = '';
  const labels=[], spent=[], budgetArr=[], forecast=[];

  status.forEach(s => {
    labels.push(s.category);
    spent.push(s.spentSoFar + s.currentCart);
    budgetArr.push(s.budget);
    forecast.push(Math.max(0, s.forecastOver + s.budget)); // month-end total

    if (s.forecastOver>0) {
      alertsDiv.innerHTML += 
        `<p>⚠️ You’re over your <strong>${s.category}</strong> budget by ₹${s.forecastOver} based on your spending patterns.</p>`;
    }
  });

  // Card ad if any over-budget
  if (alertsDiv.innerHTML) {
    cardAdDiv.style.display = 'block';
    cardAdDiv.innerHTML = `
      <strong>Partner Offer:</strong><br/>
      If you had the <em>${cardOffer.bank}</em> card, you’d get ${cardOffer.discount} off.<br/>
      <a href="${cardOffer.applyUrl}" target="_blank">
        Apply for ${cardOffer.bank} & save up to ₹${cardOffer.maxOff}
      </a>
    `;
  } else {
    cardAdDiv.style.display = 'none';
  }

  // Render Chart.js
  if (chart) chart.destroy();
  chart = new Chart(chartCtx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {label:'Budget', data: budgetArr, backgroundColor:'#3e95cd'},
        {label:'Spent+Cart', data: spent, backgroundColor:'#8e5ea2'},
        {label:'Forecast', data: forecast, type:'line', fill:false, borderColor:'#3cba9f'}
      ]
    },
    options: {
      responsive:true,
      scales: {
        y: { beginAtZero:true }
      }
    }
  });
};
