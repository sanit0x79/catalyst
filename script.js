// Initial values for the counters
let currentCount = 0;
let dailyCount = 0;
let totalCount = 0;

// Update counters every second to simulate sensor input
setInterval(() => {
    // Simulate random people entering and leaving
    let randomChange = Math.floor(Math.random() * 3) - 1; // -1, 0, or 1
    currentCount = Math.max(0, currentCount + randomChange);
    dailyCount += randomChange > 0 ? randomChange : 0;
    totalCount += randomChange > 0 ? randomChange : 0;

    // Update the HTML elements
    document.getElementById('currentCount').innerText = currentCount;
    document.getElementById('dailyCount').innerText = dailyCount;
    document.getElementById('totalCount').innerText = totalCount;
}, 1000);
