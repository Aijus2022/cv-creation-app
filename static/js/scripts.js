 // scripts.js
function submitForm(url, formData) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.getElementById('personal-details-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address').value
    };
    submitForm('/personal-details', formData);
});

document.getElementById('education-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        school: document.getElementById('school').value,
        degree: document.getElementById('degree').value,
        field_of_study: document.getElementById('field_of_study').value,
        start_date: document.getElementById('start_date').value,
        end_date: document.getElementById('end_date').value,
        description: document.getElementById('description').value
    };
    submitForm('/education', formData);
});

document.getElementById('work-experience-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        company: document.getElementById('company').value,
        job_title: document.getElementById('job_title').value,
        start_date: document.getElementById('start_date').value,
        end_date: document.getElementById('end_date').value,
        description: document.getElementById('description').value
    };
    submitForm('/work-experience', formData);
});

document.getElementById('skills-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        skill: document.getElementById('skill').value
    };
    submitForm('/skills', formData);
});

document.getElementById('certifications-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        certification: document.getElementById('certification').value
    };
    submitForm('/certifications', formData);
});

document.getElementById('hobbies-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        hobby: document.getElementById('hobby').value
    };
    submitForm('/hobbies', formData);
});

