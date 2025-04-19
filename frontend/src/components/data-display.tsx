'use client';

import React from 'react';
import { Line } from 'react-chartjs-2';
import { ChartOptions } from 'chart.js';

interface DataChartProps {
  messages: any[];
}

export const DataChart: React.FC<DataChartProps> = ({ messages }) => {
  // Prepare chart data
  const chartData = {
    labels: messages.map((_, index) => `${index + 1}`),
    datasets: [
      {
        label: 'Temperature',
        data: messages.map(msg => msg.data?.temperature || 0),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Humidity',
        data: messages.map(msg => msg.data?.humidity || 0),
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
      {
        label: 'Pressure',
        data: messages.map(msg => msg.data?.pressure || 0),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
    ],
  };
  
  const chartOptions: ChartOptions<'line'> = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'IoT Sensor Data',
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-6">
      <h2 className="text-xl font-semibold mb-2">Sensor Data Chart</h2>
      {messages.length > 0 ? (
        <div className="h-64">
          <Line data={chartData} options={chartOptions} />
        </div>
      ) : (
        <p className="text-gray-500">No data available. Waiting for messages...</p>
      )}
    </div>
  );
};

interface MessageLogProps {
  messages: any[];
}

export const MessageLog: React.FC<MessageLogProps> = ({ messages }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-2">Message Log</h2>
      <div className="overflow-auto max-h-64 border rounded p-2">
        {messages.length > 0 ? (
          messages.map((msg, index) => (
            <div key={index} className="border-b py-2 last:border-b-0">
              <div className="flex justify-between text-sm">
                <span className="font-medium">Device: {msg.device_id}</span>
                <span className="text-gray-500">Message {index + 1}</span>
              </div>
              <pre className="text-xs bg-gray-100 p-2 mt-1 rounded overflow-x-auto">
                {JSON.stringify(msg, null, 2)}
              </pre>
            </div>
          ))
        ) : (
          <p className="text-gray-500 p-2">No messages received yet.</p>
        )}
      </div>
    </div>
  );
};
