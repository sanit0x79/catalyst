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
            const response = await fetch('http://192.168.241.109/');
            const data = await response.json();
            console.log('Data:', data);
            updateCount(data.count);
            return data.count;
        } catch (error) {
            console.error('Error fetching occupancy data:', error);
            return null;
        }
    }

    function updateCount(count) {
        document.getElementById('total-count').textContent = count !== null ? count : 'N/A';
    }

    async function updateTotalOccupancy() {
        const total = await fetchOccupancyData();
        if (total === null) return; // Exit if fetchOccupancyData failed

        const now = new Date();
        const timeLabel = `${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`;

        if (totalOccupancyData.labels.length > 60) {
            totalOccupancyData.labels.shift();
            totalOccupancyData.datasets[0].data.shift();
        }

        totalOccupancyData.labels.push(timeLabel);
        totalOccupancyData.datasets[0].data.push(total);

        totalOccupancyChart.update();
    }

    // Update every second
    updateTotalOccupancy();
    setInterval(updateTotalOccupancy, 1000);
});
