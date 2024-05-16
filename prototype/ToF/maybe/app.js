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

    function updateRoomCounts() {
        // Simulatie
        const roomACount = Math.floor(Math.random() * 20);
        const roomBCount = Math.floor(Math.random() * 20);

        document.getElementById('roomA-count').textContent = roomACount;
        document.getElementById('roomB-count').textContent = roomBCount;

        return roomACount + roomBCount;
    }

    function updateTotalOccupancy() {
        const total = updateRoomCounts();
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

    // Elke 5 seconden bijwerken
    updateTotalOccupancy();
    setInterval(updateTotalOccupancy, 5000);
});
