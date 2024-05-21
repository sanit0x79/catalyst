document.addEventListener('DOMContentLoaded', function() {
    let totalOccupancyData = {
        labels: [], 
        datasets: [{
            label: 'Totaal aantal mensen in het gebouw',
            data: [],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    };

    const ctxTotal = document.getElementById('totalOccupancyChart').getContext('2d');
    const totalOccupancyChart = new Chart(ctxTotal, {
        type: 'line',
        data: totalOccupancyData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    async function fetchOccupancyData() {
        try {
            const response = await fetch('http://<ESP32_IP_ADDRESS>/');
            const data = await response.json();
            return data.count;
        } catch (error) {
            console.error('Error fetching occupancy data:', error);
        }
    }

    async function updateTotalOccupancy() {
        const total = await fetchOccupancyData();
        const now = new Date();
        const timeLabel = `${now.getHours()}:${now.getMinutes()}`;

        if (totalOccupancyData.labels.length > 60) { 
            totalOccupancyData.labels.shift();
            totalOccupancyData.datasets[0].data.shift();
        }

        totalOccupancyData.labels.push(timeLabel);
        totalOccupancyData.datasets[0].data.push(total);

        totalOccupancyChart.update();
    }

    // Update every 5 seconds
    updateTotalOccupancy();
    setInterval(updateTotalOccupancy, 5000);
});
