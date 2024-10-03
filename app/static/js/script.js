document.addEventListener('DOMContentLoaded', function() {
    // Add subtle hover effect on header
    const header = document.querySelector('header h1');
    header.addEventListener('mouseover', () => {
        header.style.color = '#34495E';
    });
    header.addEventListener('mouseout', () => {
        header.style.color = '#4A90E2';
    });
});
