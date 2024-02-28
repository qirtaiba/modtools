// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Define hex code color values
var colors = [
  '#007bff',       // January - Bootstrap primary
  '#28a745',       // February - Bootstrap success
  '#17a2b8',       // March - Bootstrap info
  '#dc3545',       // April - Bootstrap danger
  '#ffc107',       // May - Bootstrap warning
  '#a0a0ff',       // June - Variation 1
  '#8bf78b',       // July - Variation 2
  '#88d7ff',       // August - Variation 3
  '#ff8b8b',       // September - Variation 4
  '#ffd28b',       // October - Variation 5
  '#050579',       // November - Variation 6
  '#048c04'        // December - Variation 7
];

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       backgroundColor: colors,
      hoverBackgroundColor: colors,
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});

// Pie Chart Example
var ctx2 = document.getElementById("myPieChart2");
var myPieChart2 = new Chart(ctx2, {
  type: 'doughnut',
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       backgroundColor: colors,
      hoverBackgroundColor: colors,
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});

// Outbound call rating
fetch('/get_outbound_call_ratings_average')
  .then(response => response.json())
  .then(data => {
    // Process the fetched data and update the chart
    if(data.length !== 0) {
      var averageValues = parseFloat(data[0][1]).toFixed(2);
      var month = data[0][0] - 1;
      myPieChart.data.datasets[0].data[month] = averageValues;
      myPieChart.update();
      }
  })
  .catch(error => console.log(error));

// Inbound call rating
fetch('/get_inbound_call_ratings_average')
  .then(response => response.json())
  .then(data => {
    // Process the fetched data and update the chart
    if(data.length !== 0) {
      var averageValues = parseFloat(data[0][1]).toFixed(2);
      var month = data[0][0] - 1;
      myPieChart2.data.datasets[0].data[month] = averageValues;
      myPieChart2.update();
    }
  })
  .catch(error => console.log(error));
