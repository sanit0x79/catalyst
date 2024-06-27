let currentCount = 0;
let dailyCount = 0;
let totalCount = 0;
let monthlyCount = 0;

function resetDailyCount() {
    dailyCount = 0;
    document.getElementById('dailyCount').innerText = dailyCount;
}

function resetMonthlyCount() {
    monthlyCount = 0;
    document.getElementById('monthlyCount').innerText = monthlyCount;
}

async function updateCountsFromServer() {
    try {
        const response = await fetch('http://192.168.89.39/data'); // Change this to the correct IP if needed
        const serverData = await response.json();

        if (serverData.count !== undefined) {
            let previousCount = currentCount;
            currentCount = serverData.count;

            let countDifference = currentCount - previousCount;
            if (countDifference > 0) {
                dailyCount += countDifference;
                monthlyCount += countDifference;
                totalCount += countDifference;
            }

            // Update the HTML elements
            document.getElementById('currentCount').innerText = currentCount;
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

resetDailyCount();
resetMonthlyCount();
updateCountsFromServer();
