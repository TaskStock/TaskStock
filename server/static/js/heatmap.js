// const heat_options = {
//     chart: {
//         type: 'heatmap'
//     },
//     // plotOptions: {
//     //     heatmap: {
//     //         onClick: function(event, chartContext, config) {
//     //             const cellData = config.dataPoint;
//     //             const selectedDate = new Date(cellData.y);
//     //             // 여기에서 선택된 날짜에 대한 동작을 실행하면 됩니다.
//     //             // 예를 들어, 해당 날짜의 일정 목록을 보여주는 팝업을 띄울 수 있습니다.
//     //             console.log(`Clicked on date: ${selectedDate.toDateString()}`);
//     //         }
//     //     }
//     // },
//     dataLabels: {
//         enabled: false
//     },
//     // xaxis: {
//     //     type: 'datetime' // 날짜 형식 사용
//     // },
//     options: {
//         series: [
//         {
//             name: "Week 1",
//             data: [{
//                 x: 'Mon',
//                 y: '2023-07-31'
//             }, {
//                 x: 'Tue',
//                 y: '2023-08-01'
//             }, {
//                 x: 'Wed',
//                 y: '2023-08-02'
//             }, {
//                 x: 'Thu',
//                 y: '2023-08-03'
//             }, {
//                 x: 'Fri',
//                 y: '2023-08-04'
//             }, {
//                 x: 'Sat',
//                 y: '2023-08-05'
//             }, {
//                 x: 'Sun',
//                 y: '2023-08-06'
//             }  
//         ]
//         },




//         ]
//     }

// };


// const heatmap_chart = new ApexCharts(document.querySelector("#heatmap"), heat_options);
// heatmap_chart.render();



function generateData(count, yrange) {
  var i = 0;
  var series = [];
  while (i < count) {
    var x = "w" + (i + 1).toString();
    var y =
      Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

    series.push({
      x: x,
      y: y
    });
    i++;
  }
  return series;
}

const heat_options = {
  series: [
    {
      name: "Jan",
      data: generateData(20, {
        min: -30,
        max: 55
      })
    },
    {
      name: "Feb",
      data: generateData(20, {
        min: -30,
        max: 55
      })
    },
    {
      name: "Mar",
      data: generateData(20, {
        min: -30,
        max: 55
      })
    },
    {
      name: "Apr",
      data: generateData(20, {
        min: -30,
        max: 55
      })
    },
    {
      name: "May",
      data: generateData(20, {
        min: -30,
        max: 55
      })
    },
    {
      name: "Jun",
      data: generateData(20, {
        min: -30,
        max: 55
      })
    },
    {
      name: "Jul",
      data: generateData(20, {
        min: -30,
        max: 55
      })
    },
    {
      name: "Aug",
      data: generateData(20, {
        min: -30,
        max: 55
      })
    },
    {
      name: "Sep",
      data: generateData(20, {
        min: -30,
        max: 55
      })
    }
  ],
  chart: {
    height: 350,
    type: "heatmap"
  },
  plotOptions: {
    heatmap: {
      shadeIntensity: 0.5,
      radius: 0,
      useFillColorAsStroke: true,
      colorScale: {
        ranges: [
          {
            from: -30,
            to: 5,
            name: "low",
            color: "#a7cef0"
          },
          {
            from: 6,
            to: 20,
            name: "medium",
            color: "#409ff2"
          },
          {
            from: 21,
            to: 45,
            name: "high",
            color: "#f0b9bc"
          },
          {
            from: 46,
            to: 55,
            name: "extreme",
            color: "#ff6f6d"
          }
        ]
      }
         
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    width: 1
  },
  title: {
    text: "HeatMap Chart with Color Range"
  }
};

let heatmap_render = new ApexCharts(document.getElementById("heatmap"), heat_options);
heatmap_render.render();
