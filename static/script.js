// Show example when focused
const inputFields = [
    'pregnancies',
    'glucose',
    'blood_pressure',
    'skin_thickness',
    'insulin',
    'bmi',
    'diabetes_pedigree_function',
    'age'
];

inputFields.forEach(field => {
    const input = document.getElementById(field);
    const example = document.getElementById(`${field}-example`);

    input.addEventListener('focus', function () {
        example.style.display = 'block';
    });

    input.addEventListener('blur', function () {
        example.style.display = 'none';
    });
});

document.getElementById('riskForm').addEventListener('submit', function (e) {
    e.preventDefault();
    document.getElementById('error-message').innerText = '';

    const pregnancies = parseInt(document.getElementById('pregnancies').value);
    const glucose = parseFloat(document.getElementById('glucose').value);
    const bloodPressure = parseFloat(document.getElementById('blood_pressure').value);
    const skinThickness = parseFloat(document.getElementById('skin_thickness').value);
    const insulin = parseFloat(document.getElementById('insulin').value);
    const bmi = parseFloat(document.getElementById('bmi').value);
    const pedigreeFunction = parseFloat(document.getElementById('diabetes_pedigree_function').value);
    const age = parseInt(document.getElementById('age').value);

    // Validate input values
    if (pregnancies < 0 || glucose < 0 || bloodPressure < 0 || skinThickness < 0 || insulin < 0 || bmi < 0 || pedigreeFunction < 0 || age < 0) {
        document.getElementById('error-message').innerText = 'Please enter valid non-negative values for all fields.';
        return;
    }

    const formData = new FormData(this);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const predictionElement = document.getElementById('prediction');

            // Clear previous results
            predictionElement.textContent = '';
            predictionElement.className = 'prediction'; // Reset class

            // Check if there's an error in the response
            if (data.error) {
                predictionElement.textContent = `Error: ${data.error}`;
                predictionElement.className = 'error'; // Add error class for styling
            } else {
                // Display the prediction result
                predictionElement.textContent = `Prediction: ${data.prediction}`;
                predictionElement.className = 'prediction ' +
                    (data.prediction.includes('High risk') ? 'high-risk' : 'low-risk');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const predictionElement = document.getElementById('prediction');
            predictionElement.textContent = 'An error occurred while processing your request. Please try again.';
            predictionElement.className = 'error'; // Add error class for styling
        });
});