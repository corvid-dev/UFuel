document.getElementById('testForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {
    age: parseInt(document.getElementById('age').value),
    height_in: parseFloat(document.getElementById('height').value),
    weight_lb: parseFloat(document.getElementById('weight').value),
    gender: document.getElementById('gender').value,
    activity_level: document.getElementById('activity').value,
    goal: document.getElementById('goal').value,
    breakfast_location: document.getElementById('breakfast_location').value,
    lunch_location: document.getElementById('lunch_location').value,
    dinner_location: document.getElementById('dinner_location').value
  };

  const output = document.getElementById('output');
  output.textContent = 'Running...\n';

  try {
    const res = await fetch('/generate-plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Request failed');
    }

    output.textContent = JSON.stringify(data, null, 2);
    renderTable(data);
  } catch (err) {
    output.textContent = 'Error:\n' + err.message;
  }
});