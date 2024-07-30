import React, { useEffect, useState } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import axios from 'axios';

function DataChart() {
  const [chartOptions, setChartOptions] = useState({
    title: {
      text: 'Sensor Data'
    },
    xAxis: {
      type: 'datetime'
    },
    series: []
  });

  useEffect(() => {
    const fetchColumns = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/data/column_data/');
        const columns = response.data.columns;
        const initialSeries = columns.map(col => ({
          name: col.charAt(0).toUpperCase() + col.slice(1),
          data: []
        }));

        setChartOptions(prevOptions => ({
          ...prevOptions,
          series: initialSeries
        }));

        return columns;
      } catch (error) {
        console.error('Error fetching columns:', error);
        return [];
      }
    };

    const fetchData = async (columns) => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/data/read_data/');
        const data = response.data;

        const seriesData = columns.map(col => ({
          name: col.charAt(0).toUpperCase() + col.slice(1),
          data: data.map(entry => [
            new Date(entry.time).getTime(),
            typeof entry[col.toLowerCase()] === 'boolean' ? (entry[col.toLowerCase()] ? 1 : 0) : entry[col.toLowerCase()]
          ])
        }));

        setChartOptions(prevOptions => ({
          ...prevOptions,
          series: seriesData
        }));
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const initializeChart = async () => {
      const columns = await fetchColumns();
      if (columns.length > 0) {
        await fetchData(columns);
      }
    };

    initializeChart();
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
