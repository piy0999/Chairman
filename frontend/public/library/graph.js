var receiveddata;

$.get(window.location.origin + ':3000/seats', function(data) {
  receiveddata = data;
  console.log(receiveddata);
});

var ctx = document.getElementById('myChart').getContext('2d');

var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Zone 1', 'Zone 2', 'Zone 3'],
    datasets: [
      {
        label: '# of Empty Seats',
        data: [70, 0, 0],
        backgroundColor: [
          'rgba(0, 255, 0, 0.6)',
          'rgba(0, 255, 0, 0.6)',
          'rgba(0, 255, 0, 0.6)'
        ],
        borderColor: [
          'rgba(0, 255, 0, 0.6)',
          'rgba(0, 255, 0, 0.6)',
          'rgba(0, 255, 0, 0.6)'
        ],
        borderWidth: 1
      },
      {
        label: '# of occupied seats',
        data: [30, 100, 100],
        backgroundColor: [
          'rgba(255, 0, 0, 0.6)',
          'rgba(255, 0, 0, 0.6)',
          'rgba(255, 0, 0, 0.6)'
        ],
        borderColor: [
          'rgba(255, 0, 0, 0.6)',
          'rgba(255, 0, 0, 0.6)',
          'rgba(255, 0, 0, 0.6)'
        ],
        borderWidth: 1
      }
    ]
  },
  options: {
    scales: {
      yAxes: [
        {
          stacked: true,
          ticks: {
            beginAtZero: true
          }
        }
      ],
      xAxes: [
        {
          stacked: true,
          ticks: {
            beginAtZero: true
          }
        }
      ]
    }
  }
});
