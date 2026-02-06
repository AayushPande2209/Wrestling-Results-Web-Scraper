'use client';

import React from 'react';

interface ChartWrapperProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export function ChartWrapper({ title, children, className = '' }: ChartWrapperProps) {
  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">{title}</h3>
      <div className="w-full h-64">
        {children}
      </div>
    </div>
  );
}