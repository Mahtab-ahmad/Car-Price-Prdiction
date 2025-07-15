document.getElementById('prediction-form').addEventListener('submit', async function(e) {
    e.preventDefault(); // prevent form from reloading the page

    const formData = new FormData(e.target);

    // Convert formData to JSON
    const data = {};
    formData.forEach((value, key) => {
        if (key === 'year' || key === 'km_driven' || key === 'seats') {
            data[key] = parseInt(value);
        } else if (key === 'mileage' || key === 'engine' || key === 'max_power') {
            data[key] = parseFloat(value);
        } else {
            data[key] = value;
        }
    });

    try {
        const response = await fetch('https://car-price-prdiction.onrender.com/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const result = await response.json();

        document.getElementById('result').textContent = `Predicted Price: ₹ ${result.Prediction.toFixed(2)}`;
    } catch (err) {
        document.getElementById('result').textContent = 'Network error or server not responding.';
        console.error(err);
    }
});
