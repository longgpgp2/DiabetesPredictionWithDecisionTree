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
document.getElementById('closeModalButton').addEventListener('click', function () {
    const modal = bootstrap.Modal.getInstance(document.getElementById('resultModal'));
    modal.hide();
    document.getElementById('resultModal').classList.remove('show');

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
            const modal = document.getElementById('resultModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            const modalContent = document.getElementById('modalContent');

            modalContent.className = 'modal-content';

            if (data.error) {
                modalTitle.textContent = 'Error';
                modalBody.innerHTML = `<p class="text-danger">${data.error}</p>`;
                modalContent.classList.add('modal-high-risk');
            } else {
                modalTitle.textContent = 'Prediction Result';
                modalBody.innerHTML = `<p class="fw-bold">${data.prediction}</p>`;
                modalContent.classList.add(data.prediction === 'High risk' ? 'modal-high-risk' : 'modal-low-risk');
            }

            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        })
        .catch(error => {
            console.error('Error:', error);
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            const modal = new bootstrap.Modal(document.getElementById('resultModal'));

            modalTitle.textContent = 'Error';
            modalBody.innerHTML = '<p class="text-danger">An error occurred while processing your request. Please try again.</p>';
            modal.show();
        });

});

document.getElementById('closeModalButton').addEventListener('click', function () {
    const modal = document.getElementById('resultModal');
    modal.style.display = 'none';
    document.body.style.overflow = '';
});

document.getElementById('footerCloseButton').addEventListener('click', function () {
    const modal = document.getElementById('resultModal');
    modal.style.display = 'none';
    document.body.style.overflow = '';
});
