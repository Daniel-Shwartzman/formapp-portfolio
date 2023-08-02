function removeAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.classList.add('fade-out');
        }, 2000); // 5000 milliseconds (5 seconds) - you can adjust this value as needed
    });
}

// Call the function to remove the alerts when the page loads
document.addEventListener('DOMContentLoaded', () => {
    removeAlerts();

    // After the fade-out effect is complete, remove the alert from the DOM
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        alert.addEventListener('animationend', () => {
            alert.style.display = 'none';
        });
    });
});