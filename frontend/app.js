const form = document.querySelector('#risk-form');
const apiBase = window.MEDGUARD_API_URL || 'http://localhost:8000/api/v1';
const token = window.localStorage.getItem('medguard_access_token');
const setLoading = (loading) => {
  const button = form.querySelector('button');
  button.disabled = loading;
  button.textContent = loading ? 'Assessing…' : 'Assess cardiovascular risk →';
};
const applyResult = (score, message) => {
  document.querySelector('#risk-score').textContent = `${score}%`;
  const high = score >= 50;
  document.querySelector('#risk-label').textContent = high ? 'HIGH RISK' : 'MODERATE RISK';
  document.querySelector('#result-title').textContent = high ? 'Clinical review recommended' : 'Monitor and review routinely';
  document.querySelector('#result-text').textContent = message || (high ? 'This local demo estimate identifies elevated contributing factors.' : 'The selected inputs produce a lower research-risk estimate.');
};
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  setLoading(true);
  try {
    if (!token) throw new Error('Demo mode');
    const payload = {...data, fbs: 0, restecg: 0, exang: 0, oldpeak: 0, slope: 1, ca: 0, thal: 2};
    const response = await fetch(`${apiBase}/predictions/cardiovascular-risk`, {method: 'POST', headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`}, body: JSON.stringify(payload)});
    if (!response.ok) throw new Error('Assessment service unavailable');
    const result = await response.json();
    applyResult(result.risk_score, result.disclaimer);
  } catch (error) {
    const score = Math.min(95, Math.max(8, Math.round((Number(data.age) * .35 + Number(data.trestbps) * .25 + Number(data.chol) * .08) / 1.25)));
    applyResult(score);
  } finally { setLoading(false); }
});
