const ctx = document.getElementById('chart').getContext('2d');
let chart;

document.getElementById('analyze-btn').addEventListener('click', async () => {
  const startDate = document.getElementById('start-date').value;

  if (!startDate) {
    alert("Please select a start date for prediction.");
    return;
  }

  console.log("Sending request with date:", startDate);

  const response = await fetch('http://127.0.0.1:5000/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ start_date: startDate })
  });

  console.log("Response status:", response.status);

  const result = await response.json();

  console.log("Server responded:", result);

  if (result.error) {
    alert("Error: " + result.error);
    return;
  }

  const labelsPred = result.predictions.map(e => e.date);
  const dataPred = result.predictions.map(e => e.temp);

  console.log("Prediction dates:", labelsPred);
  console.log("Prediction temps:", dataPred);

  const datasets = [{
    label: 'Predicted Average Temperature (Next 7 Days)',
    data: dataPred,
    borderColor: 'red',
    backgroundColor: 'red',
    fill: false,
    tension: 0.2,
    pointRadius: 5
  }];

  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: 'line',
    data: { labels: labelsPred, datasets },
    options: {
      scales: {
        x: { 
          display: true, 
          title: { 
            display: true, 
            text: 'Date',
            color: 'black'       
          },
          ticks: {
            color: 'black'       
          }
        },
        y: { 
          display: true, 
          title: { 
            display: true, 
            text: 'Temperature (°C)',
            color: 'black'       
          },
          ticks: {
            color: 'black'       
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: 'black'      
          }
        }
      }
    }
  });
});
