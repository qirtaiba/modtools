// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{
  label: "Outbound Calls",
  lineTension: 0.3,
  backgroundColor: "rgba(78, 115, 223, 0.05)",
  borderColor: "rgba(78, 115, 223, 1)",
  pointRadius: 3,
  pointBackgroundColor: "rgba(78, 115, 223, 1)",
  pointBorderColor: "rgba(78, 115, 223, 1)",
  pointHoverRadius: 3,
  pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
  pointHoverBorderColor: "rgba(78, 115, 223, 1)",
  pointHitRadius: 10,
  pointBorderWidth: 2,
  data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 10,
          callback: function(value, index, values) {
          return value ;
        }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': \uD83D\uDCDE' + number_format(tooltipItem.yLabel);
        }
      }
    }
  }
});

// Area Chart Example 2
var ctx2 = document.getElementById("myAreaChart2");
var myLineChart2 = new Chart(ctx2, {
  type: 'line',
  data: {
    // Modify the data for the new chart as needed
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [
      {
        label: "Inbound Calls",
        lineTension: 0.3,
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        pointRadius: 3,
        pointBackgroundColor: "rgba(255, 99, 132, 1)",
        pointBorderColor: "rgba(255, 99, 132, 1)",
        pointHoverRadius: 3,
        pointHoverBackgroundColor: "rgba(255, 99, 132, 1)",
        pointHoverBorderColor: "rgba(255, 99, 132, 1)",
        pointHitRadius: 10,
        pointBorderWidth: 2,
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      }
    ]
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 10,
          callback: function(value, index, values) {
            return value;
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }]
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': \uD83D\uDCDE' + number_format(tooltipItem.yLabel);
        }
      }
    }
  }
});

// Area Chart Example 3
var ctx3 = document.getElementById("myAreaChart3");
var myLineChart3 = new Chart(ctx3, {
  type: 'line',
  data: {
    // Modify the data for the new chart as needed
    labels: [],
    datasets: [
      {
        label: "Outbound Calls Monthly",
        lineTension: 0.3,
        backgroundColor: "rgba(78, 115, 223, 0.05)",
        borderColor: "rgba(78, 115, 223, 1)",
        pointRadius: 3,
        pointBackgroundColor: "rgba(78, 115, 223, 1)",
        pointBorderColor: "rgba(78, 115, 223, 1)",
        pointHoverRadius: 3,
        pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
        pointHoverBorderColor: "rgba(78, 115, 223, 1)",
        pointHitRadius: 10,
        pointBorderWidth: 2,
        data: []
      }
    ]
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'day'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 10
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 10,
          callback: function(value, index, values) {
            return value;
          }
        },
         gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': \uD83D\uDCDE' + number_format(tooltipItem.yLabel);
        }
      }
    }
  }
});

// Area Chart Example 4
var ctx4 = document.getElementById("myAreaChart4");
var myLineChart4 = new Chart(ctx4, {
  type: 'line',
  data: {
    // Modify the data for the new chart as needed
    labels: [],
    datasets: [
      {
        label: "Inbound Calls Monthy",
        lineTension: 0.3,
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        pointRadius: 3,
        pointBackgroundColor: "rgba(255, 99, 132, 1)",
        pointBorderColor: "rgba(255, 99, 132, 1)",
        pointHoverRadius: 3,
        pointHoverBackgroundColor: "rgba(255, 99, 132, 1)",
        pointHoverBorderColor: "rgba(255, 99, 132, 1)",
        pointHitRadius: 10,
        pointBorderWidth: 2,
        data: []
      }
    ]
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'day'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 10
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 10,
          callback: function(value, index, values) {
            return value;
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }]
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': \uD83D\uDCDE' + number_format(tooltipItem.yLabel);
        }
      }
    }
  }
});

// Get the current date
var currentDate = new Date();
// Get the number of days in the current month
var daysInMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();

// Generate the labels for the x-axis
var labels = [];
var datas = [];
var datas1 = [];
for (var i = 1; i <= daysInMonth; i++) {
  // Show every 5th day as a label, and the rest as empty string
  var label = i.toString();
  labels.push(label);
  datas.push(0);
  datas1.push(0);
}

// Update the chart data with the new labels
myLineChart3.data.labels = labels;
myLineChart3.data.datasets[0].data = datas;
myLineChart4.data.labels = labels;
myLineChart4.data.datasets[0].data = datas1;

// Update the chart
myLineChart3.update();
myLineChart4.update();

// Fetch the inbound call data from the server
fetch('/get_inbound_calls_by_month')
  .then(response => response.json())
  .then(data => {
    // Update the chart data with the fetched data
    data.forEach(call => {
      var monthIndex = call[1] - 1;
      myLineChart2.data.datasets[0].data[monthIndex] = call[2];
    });
    // Update the chart
    myLineChart2.update();
  })
  .catch(error => console.log(error));

// Fetch the outbound call data from the server
fetch('/get_outbound_calls_by_month')
  .then(response => response.json())
  .then(data => {
    // Update the chart data with the fetched data
    data.forEach(call => {
      var monthIndex = call[1] - 1; // Convert month to zero-based index
      myLineChart.data.datasets[0].data[monthIndex] = call[2];
    });
    // Update the chart
    myLineChart.update();
  })
  .catch(error => console.log(error));


fetch('/get_outbound_calls_of_current_month')
  .then(response => response.json())
  .then(data => {
    // Update the chart data with the fetched data
    data.forEach(call => {
      var monthIndex = call[2] - 1; // Convert month to zero-based index
      myLineChart3.data.datasets[0].data[monthIndex] = call[3];
    });
    // Update the chart
    myLineChart3.update();
  })
  .catch(error => console.log(error));

fetch('/get_inbound_calls_of_current_month')
  .then(response => response.json())
  .then(data => {
    // Update the chart data with the fetched data
    data.forEach(call => {

      var monthIndex = call[2] - 1; // Convert month to zero-based index
      myLineChart4.data.datasets[0].data[monthIndex] = call[3];
    });
    // Update the chart
    myLineChart4.update();
  })
  .catch(error => console.log(error));


