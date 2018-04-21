window.onload = function() {
  var receiveddata;
  $.get(window.location.origin + ':8080/seats', function(data) {
    receiveddata = (data[0]['nOfSeats'] - data[0]['nOfPeople']) % 100;
    console.log(receiveddata);
    var ctx = document.getElementById('myChart').getContext('2d');

    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Zone 1', 'Zone 2', 'Zone 3'],
        datasets: [
          {
            label: '# of Empty Seats',
            data: [0, receiveddata, 0],
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
            data: [100, 100 - receiveddata, 100],
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
  });
};
