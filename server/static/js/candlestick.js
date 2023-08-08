var options = {
  series: [{
  name: 'candle',
  data: dataset
}],
  chart: {
  height: '50%',
  type: 'candlestick',
  zoom: {
    enabled: false,
  }

},
plotOptions: {
  candlestick: {
    colors: {
      upward: 'red',
      downward: 'blue',
    }
  }
},

annotations: {
  xaxis: [
    {
      // x: 'Oct 06 14:00',
      // borderColor: '#00E396',
      borderColor: '#000',
      label: {
        borderColor: '#00E396',
        style: {
          fontSize: '12px',
          color: '#fff',
          background: '#00E396'
        },
        orientation: 'horizontal',
        offsetY: 7,
        // text: 'Annotation Test'
      }
    }
  ]
},
tooltip: {
  enabled: true,
},
xaxis: {
  type: 'category',
  labels: {
    // formatter: function(val) {
    //   return dayjs(val).format('MMM DD HH:mm')
    // }
    show: false,
  }
},
yaxis: {
  tooltip: {
    enabled: true
  }
}
};

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();