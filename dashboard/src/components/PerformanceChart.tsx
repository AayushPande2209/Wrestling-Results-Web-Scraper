'use client';

import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ChartWrapper } from './ChartWrapper';

interface PerformanceDataPoint {
  date: string;
  wins: number;
  matches: number;
  pins: number;
}

interface PerformanceChartProps {
  data: PerformanceDataPoint[];
  title?: string;
}

type MetricType = 'wins' | 'matches' | 'pins';

export function PerformanceChart({ data, title = "Performance Over Time" }: PerformanceChartProps) {
  const [selectedMetric, setSelectedMetric] = useState<MetricType>('wins');

  const metricConfig = {
    wins: { color: '#10B981', label: 'Wins' },
    matches: { color: '#3B82F6', label: 'Total Matches' },
    pins: { color: '#F59E0B', label: 'Pins' }
  };

  return (
    <ChartWrapper title={title}>
      <div className="mb-4">
        <div className="flex space-x-2">
          {Object.entries(metricConfig).map(([key, config]) => (
            <button
              key={key}
              onClick={() => setSelectedMetric(key as MetricType)}
              className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                selectedMetric === key
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
              }`}
            >
              {config.label}
            </button>
          ))}
        </div>
      </div>
      
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => new Date(value).toLocaleDateString()}
          />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip 
            labelFormatter={(value) => new Date(value).toLocaleDateString()}
            formatter={(value: number | undefined) => [value || 0, metricConfig[selectedMetric].label]}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey={selectedMetric}
            stroke={metricConfig[selectedMetric].color}
            strokeWidth={2}
            dot={{ fill: metricConfig[selectedMetric].color, strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </ChartWrapper>
  );
}