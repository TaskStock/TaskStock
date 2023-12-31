document.addEventListener("DOMContentLoaded", function(){  
  const one_week = document.querySelector("#one_week");
  const one_month = document.querySelector("#one_month");
  const three_month = document.querySelector("#three_month");
  const six_month = document.querySelector("#six_month");
  const one_year = document.querySelector("#one_year");

  if(one_week){
    one_week.addEventListener("click", function(){
      request_chart("7");
      localStorage.setItem('chart_radio', "7");
    });
    one_month.addEventListener("click", function(){
      request_chart("30");
      localStorage.setItem('chart_radio', "30");
    });
    three_month.addEventListener("click", function(){
      request_chart("90");
      localStorage.setItem('chart_radio', "90");
    });
    six_month.addEventListener("click", function(){
      request_chart("180");
      localStorage.setItem('chart_radio', "180");
    });
    one_year.addEventListener("click", function(){
      request_chart("365");
      localStorage.setItem('chart_radio', "365");
    });
  
    let chart_radio=localStorage.getItem('chart_radio');
    if(chart_radio==null){
      one_week.click();
    }else{
      request_chart(chart_radio);
      if(chart_radio == "7"){
        one_week.checked = true;
      }else if(chart_radio == "30"){
        one_month.checked = true;
      }else if(chart_radio == "90"){
        three_month.checked = true;
      } else if(chart_radio == "180"){
        six_month.checked = true;
      } else if(chart_radio == "365"){
        one_year.checked = true;
      }
    }
  }

});

const request_chart = async (day) =>{
  const formData = new FormData();
  formData.append("day", day);

  formData.append("username", global_chart_target_username);

  const url = "/main/chart_ajax/";
  const res = await fetch(url, {
      method:"POST",
      headers:{},
      body: formData,
  });
  const {dataset: dataset} = await res.json();
  showChart(dataset);
}

const showChart = (dataset) => {
  const chartdiv = document.querySelector("#chart");
  chartdiv.innerHTML="";
  
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
    },
    toolbar: {
      show: false,
    },
  },
  plotOptions: {
    candlestick: {
      colors: {
        upward: '#DD1717',
        downward: '#124392',
      },
      wick: { useFillColor: true },
    }
  },
  grid: {
    yaxis: {
      lines: {
        show: true,
      }
    }
  },
  annotations: {
    xaxis: [
      {
       
        borderColor: '#000',
        label: {
          borderColor: '#00E396',
          style: {
            fontSize: '12px',
            color: '#fff',
            background: '#00E396'
          },
          orientation: 'horizontal',
        
        }
      }
    ]
  },

  xaxis: {
    labels: {
      show: false,
    },
    tooltip:{
      // offsetX: true,
    },
    type: "datetime",
  },
  yaxis: {
    labels: {
      // show: false,
      style: {
        colors: 'var(--text-color)'
      },
    },
  },
  tooltip: {
    enabled: false,
  },
 
  };

  var chart = new ApexCharts(document.querySelector("#chart"), options);
  chart.render();
}