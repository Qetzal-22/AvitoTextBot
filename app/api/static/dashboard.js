document.addEventListener('DOMContentLoader', function () {
    const ctx1 = document.getElementById('RequestChart');
    const ctx2 = document.getElementById('RevenueChart');


    new Chart(ctx1, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            dataset: [{
                label: 'Request',
                data: [1, 2, 3, 2, 1, 2, 4],//requestsValues,
                borderColor: 'rgb(75,192,192)',
                backgroundColor: 'rgba(75,192,192,0.2)',
            }]
        }
    });

    new Chart(ctx2, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            dataset: [{
                label: 'Revenue',
                data: [1, 2, 3, 2, 1, 2, 4], //revenueValues,
                borderColor: 'rgb(75,192,192)',
                backgroundColor: 'rgba(75,192,192,0.2)',
            }]
        }
    })
});