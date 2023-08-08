


var options = {
  series: [{
  name: 'candle',
  data: [
    {
      x: 1545000000000, // Wednesday
      y: []
    },
      {
        x: 1546275600000, // Wednesday
        y: [6629.81, 6650.5, 6623.04, 6633.33]
      },
      {
        x: 1546362000000, // Thursday
        y: [6632.01, 6643.59, 6620, 6630.11]
      },
      {
        x: 1546448400000, // Friday
        y: [6630.71, 6648.95, 6623.34, 6635.65]
      },
      // { // SATURDAY : NO DATA
      //   x: 1546534800000,
      //   y: [6635.65, 6651, 6629.67, 6638.24]
      // },
      // { // SUNDAY : NO DATA
      //   x: 1546621200000,
      //   y: [6624.53, 6636.03, 6621.68, 6624.31]
      // },
      {
        x: 1546707600000, // Monday
        y: [6624.61, 6632.2, 6617, 6626.02]
      },
      {
        x: 1546794000000, // Tuesday
        y: [6635.65, 6651, 6629.67, 6638.24]
      },]

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