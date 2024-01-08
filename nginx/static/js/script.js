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

document.addEventListener("DOMContentLoaded", function () {
    // Set the default tab when the page loads
    setDefaultTab();

    // Add click event listeners to tab links
    const tabLinks = document.querySelectorAll(".tablink");
    tabLinks.forEach((tabLink) => {
        tabLink.addEventListener("click", () => {
            const tabName = tabLink.getAttribute("data-tab");
            openTab(tabName);

            // Update the URL with the hash fragment
            window.location.hash = tabName;
        });
    });

    // Check if a hash fragment is present in the URL
    if (window.location.hash) {
        const tabName = window.location.hash.substr(1); // Remove the '#' character
        const tabLink = document.querySelector(`.tablink[data-tab="${tabName}"]`);
        if (tabLink) {
            // If the tab exists, simulate a click on the tab link
            tabLink.click();
        }
    }
});

function setDefaultTab() {
    // Get the first tab and open it
    var firstTab = document.querySelector(".tabcontent");
    firstTab.style.display = "block";

    // Get the corresponding tab link and add the 'active' class
    var firstTabLink = document.querySelector('button.tablink[data-tab="' + firstTab.id + '"]');
    firstTabLink.classList.add("active");
}

function openTab(tabName) {
    // Hide all tab contents
    var tabContents = document.getElementsByClassName("tabcontent");
    for (var i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = "none";
    }

    // Show the selected tab content
    document.getElementById(tabName).style.display = "block";

    // Remove 'active' class from all tab links
    var tabLinks = document.getElementsByClassName("tablink");
    for (var i = 0; i < tabLinks.length; i++) {
        tabLinks[i].classList.remove("active");
    }

    // Add 'active' class to the clicked tab link
    var clickedTabLink = document.querySelector(`button.tablink[data-tab="${tabName}"]`);
    clickedTabLink.classList.add("active");
}
