'use client';

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ChartWrapper } from './ChartWrapper';

interface WinTypeData {
  type: string;
  count: number;
}

interface WinTypesChartProps {
  data: WinTypeData[];
  title?: string;
}

export function WinTypesChart({ data, title = "Win Types Distribution" }: WinTypesChartProps) {
  // Default win types if no data provided
  const defaultData = [
    { type: 'Pin', count: 0 },
    { type: 'Tech Fall', count: 0 },
    { type: 'Major', count: 0 },
    { type: 'Decision', count: 0 }
  ];

  // Merge provided data with defaults
  const chartData = defaultData.map(defaultItem => {
    const providedItem = data.find(item => item.type === defaultItem.type);
    return providedItem || defaultItem;
  });

  const hasData = chartData.some(item => item.count > 0);

  return (
    <ChartWrapper title={title}>
      {hasData ? (
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="type" 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip 
              formatter={(value: number | undefined) => [value || 0, 'Wins']}
              labelStyle={{ color: '#374151' }}
            />
            <Legend />
            <Bar 
              dataKey="count" 
              fill="#3B82F6"
              name="Wins"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <div className="flex items-center justify-center h-full text-gray-500">
          No win type data available
        </div>
      )}
    </ChartWrapper>
  );
}