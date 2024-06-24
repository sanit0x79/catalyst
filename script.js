// Initial values for the counters
let currentCount = 0;
let dailyCount = 0;
let totalCount = 0;
let monthlyCount = 0;

// Function to reset daily count at midnight
function resetDailyCount() {
    dailyCount = 0;
    document.getElementById('dailyCount').innerText = dailyCount;
}

// Function to reset monthly count on the first day of the month
function resetMonthlyCount() {
    monthlyCount = 0;
    document.getElementById('monthlyCount').innerText = monthlyCount;
}

// Check the time every second
setInterval(() => {
    let now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();
    let date = now.getDate();

    // If it's midnight, reset the daily count
    if (hours === 0 && minutes === 0 && seconds === 0) {
        resetDailyCount();
    }

    // If it's the first day of the month, reset the monthly count
    if (date === 1 && hours === 0 && minutes === 0 && seconds === 0) {
        resetMonthlyCount();
    }

    // Simulate random people entering and leaving
    let randomChange = Math.floor(Math.random() * 3) - 1; // -1, 0, or 1
    currentCount = Math.max(0, currentCount + randomChange);
    dailyCount += randomChange > 0 ? randomChange : 0;
    monthlyCount += randomChange > 0 ? randomChange : 0;
    totalCount += randomChange > 0 ? randomChange : 0;

    // Update the HTML elements
    document.getElementById('currentCount').innerText = currentCount;
    document.getElementById('dailyCount').innerText = dailyCount;
    document.getElementById('monthlyCount').innerText = monthlyCount;
    document.getElementById('totalCount').innerText = totalCount;
}, 1000);

// Initial call to set the time check interval
resetDailyCount();
resetMonthlyCount();
