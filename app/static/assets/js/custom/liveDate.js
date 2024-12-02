// liveDate.js

// Function to format and display the current date
function updateLiveDate() {
    const dateElement = document.getElementById("live-date");
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const now = new Date();
    const formattedDate = now.toLocaleDateString('en-US', options); // Adjust locale as needed
    dateElement.textContent = formattedDate;
}

// Call the function on page load
document.addEventListener("DOMContentLoaded", updateLiveDate);
