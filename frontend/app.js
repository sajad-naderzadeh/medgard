const form = document.querySelector('#risk-form');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  const score = Math.min(95, Math.max(8, Math.round((Number(data.age) * .35 + Number(data.trestbps) * .25 + Number(data.chol) * .08) / 1.25)));
  document.querySelector('#risk-score').textContent = `${score}%`;
  const high = score >= 50;
  document.querySelector('#risk-label').textContent = high ? 'HIGH RISK' : 'MODERATE RISK';
  document.querySelector('#result-title').textContent = high ? 'Clinical review recommended' : 'Monitor and review routinely';
  document.querySelector('#result-text').textContent = high ? 'This local demo estimate identifies elevated contributing factors.' : 'The selected inputs produce a lower research-risk estimate.';
});
