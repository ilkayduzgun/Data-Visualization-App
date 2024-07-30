import React, { useEffect, useState } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import axios from 'axios';

function DataChart() {
  const [data, setData] = useState([]);
  const [chartOptions, setChartOptions] = useState({
    title: {
      text: 'Sensor Data'
    },
    xAxis: {
      type: 'datetime'
    },
    series: [
      { name: 'Temperature', data: [] },
      { name: 'Pressure', data: [] },
      { name: 'Current', data: [] },
      { name: 'Error', data: [] },
    ]
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/data/read_data/');
        const data = response.data;
        console.log("Data: ", data);

        const tempData = data.map(entry => [new Date(entry.time).getTime(), entry.temp]);
        const pressureData = data.map(entry => [new Date(entry.time).getTime(), entry.pressure]);
        const currentData = data.map(entry => [new Date(entry.time).getTime(), entry.current]);
        const errorData = data.map(entry => [new Date(entry.time).getTime(), entry.error ? 1 : 0]);

        console.log(" Temp Data: ", tempData);
        console.log(" Pressure Data: ", pressureData);
        console.log(" Current Data: ", currentData);
        console.log(" Error Data: ", errorData);

        setChartOptions({
          title: {
            text: 'Sensor Data'
          },
          xAxis: {
            type: 'datetime'
          },
          series: [
            { name: 'Temperature', data: tempData },
            { name: 'Pressure', data: pressureData },
            { name: 'Current', data: currentData },
            { name: 'Error', data: errorData },
          ]
        });
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <HighchartsReact
        highcharts={Highcharts}
        options={chartOptions}
      />
    </div>
  );
}

export default DataChart;
