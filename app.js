const els = {
  kwp: document.querySelector('#kwp'),
  yield: document.querySelector('#yield'),
  tariff: document.querySelector('#tariff'),
  cost: document.querySelector('#cost'),
  kwpValue: document.querySelector('#kwpValue'),
  yieldValue: document.querySelector('#yieldValue'),
  tariffValue: document.querySelector('#tariffValue'),
  costValue: document.querySelector('#costValue'),
  annualKwh: document.querySelector('#annualKwh'),
  savings: document.querySelector('#savings'),
  payback: document.querySelector('#payback'),
};

const number = new Intl.NumberFormat('en-US', {
  maximumFractionDigits: 0,
});

function formatFjd(value) {
  return `FJD ${number.format(value)}`;
}

function updateEstimate() {
  const kwp = Number(els.kwp.value);
  const annualYield = Number(els.yield.value);
  const tariff = Number(els.tariff.value);
  const costPerKw = Number(els.cost.value);
  const annualKwh = kwp * annualYield;
  const savings = annualKwh * tariff;
  const capex = kwp * costPerKw;
  const payback = capex / savings;

  els.kwpValue.value = `${kwp.toFixed(1)} kWp`;
  els.yieldValue.value = `${number.format(annualYield)} kWh`;
  els.tariffValue.value = `FJD ${tariff.toFixed(2)}/kWh`;
  els.costValue.value = `FJD ${number.format(costPerKw)}/kW`;
  els.annualKwh.textContent = `${number.format(annualKwh)} kWh`;
  els.savings.textContent = formatFjd(savings);
  els.payback.textContent = `${payback.toFixed(2)} years`;
}

for (const input of [els.kwp, els.yield, els.tariff, els.cost]) {
  input.addEventListener('input', updateEstimate);
}

updateEstimate();
