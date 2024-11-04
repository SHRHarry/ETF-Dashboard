import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

const PieChart = ({ data }) => {
  const pieData = {
    labels: data.labels,
    datasets: [
      {
        label: '分佈',
        data: data.values,
        backgroundColor: data.values.map(() => `#${Math.floor(Math.random()*16777215).toString(16)}`),
      }
    ]
  };
  const chartOptions = {
    plugins: {
      datalabels: {
        formatter: (value) => `${value.toFixed(2)}%`, // Format to show percentage with 2 decimal places
        color: '#fff', // Label color
        font: {
          weight: 'bold',
          size: 14,
        },
      },
      legend: {
        position: 'top', // Position of the legend
      },
      tooltip: {
        callbacks: {
          label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw.toFixed(2)}%`,
        },
      },
    },
  };

  return (
    <div style={{ height: '400px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <Pie data={pieData} options={{ ...chartOptions, maintainAspectRatio: false }} />
    </div>
  );
};

export default PieChart;