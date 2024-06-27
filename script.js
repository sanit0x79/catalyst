let currentCount = 0;
let dailyCount = 0;
let totalCount = 0;
let monthlyCount = 0;

async function resetDailyCount() {
    dailyCount = 0;
    document.getElementById('dailyCount').innerText = dailyCount;
}

async function resetMonthlyCount() {
    monthlyCount = 0;
    document.getElementById('monthlyCount').innerText = monthlyCount;
}

async function updateCountsFromServer() {
    try {
        const response = await fetch('http://192.168.89.30/data');
        const serverData = await response.json();

        if (serverData) {
            dailyCount = serverData.visitors_today;
            monthlyCount = serverData.visitors_this_month;
            totalCount = serverData.total_visitors;

            // Update the HTML elements
            document.getElementById('dailyCount').innerText = dailyCount;
            document.getElementById('monthlyCount').innerText = monthlyCount;
            document.getElementById('totalCount').innerText = totalCount;
        }
    } catch (error) {
        console.error('Error fetching data from server:', error);
    }
}

setInterval(() => {
    let now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();
    let date = now.getDate();

    if (hours === 0 && minutes === 0 && seconds === 0) {
        resetDailyCount();
    }

    if (date === 1 && hours === 0 && minutes === 0 && seconds === 0) {
        resetMonthlyCount();
    }

    updateCountsFromServer();

}, 1000);

updateCountsFromServer();
