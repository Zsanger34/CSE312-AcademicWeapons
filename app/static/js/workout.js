document.addEventListener('DOMContentLoaded', function() {
    const days = document.querySelectorAll('[data-day]');

    days.forEach(day => {
        day.addEventListener('click', function() {
            const dayValue = day.getAttribute('data-day'); // Get the value of the clicked day
            window.location.href = `/workout_routine/${dayValue}`; // Redirect to the Flask route
        });
    });
});