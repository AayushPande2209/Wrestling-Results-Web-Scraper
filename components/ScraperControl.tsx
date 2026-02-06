'use client'

import { useState } from 'react'

interface ScraperStatus {
  isRunning: boolean
  message: string
  startTime?: string
  pid?: number
}

export default function ScraperControl() {
  const [status, setStatus] = useState<ScraperStatus>({
    isRunning: false,
    message: 'Ready to scrape'
  })

  const runScraper = async () => {
    try {
      setStatus({
        isRunning: true,
        message: 'Starting scraper...'
      })

      const response = await fetch('/api/run-scraper', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      const data = await response.json()

      if (data.success) {
        setStatus({
          isRunning: true,
          message: 'Scraper is running! This may take several hours...',
          startTime: data.startTime,
          pid: data.pid
        })

        // Auto-refresh data after some time (in a real app, you'd use websockets)
        setTimeout(() => {
          setStatus({
            isRunning: false,
            message: 'Scraping completed. Refresh the page to see new data.'
          })
          // Trigger a page refresh to show new data
          window.location.reload()
        }, 30000) // 30 seconds for demo - in reality this would be hours

      } else {
        setStatus({
          isRunning: false,
          message: `Error: ${data.error}`
        })
      }

    } catch (error) {
      setStatus({
        isRunning: false,
        message: `Failed to start scraper: ${error}`
      })
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Data Scraper</h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {status.message}
          </p>
          {status.startTime && (
            <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
              Started: {new Date(status.startTime).toLocaleString()}
            </p>
          )}
          {status.pid && (
            <p className="text-xs text-gray-500 dark:text-gray-500">
              Process ID: {status.pid}
            </p>
          )}
        </div>
        
        <button
          onClick={runScraper}
          disabled={status.isRunning}
          className={`px-4 py-2 rounded-md font-medium transition-colors ${
            status.isRunning
              ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600'
          }`}
        >
          {status.isRunning ? (
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Running...
            </div>
          ) : (
            'Run Scraper'
          )}
        </button>
      </div>
      
      {status.isRunning && (
        <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-md border border-blue-200 dark:border-blue-800">
          <div className="flex">
            <div className="flex-shrink-0">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600 dark:border-blue-400"></div>
            </div>
            <div className="ml-3">
              <p className="text-sm text-blue-800 dark:text-blue-200">
                Scraping in progress...
              </p>
              <p className="text-xs text-blue-600 dark:text-blue-300 mt-1">
                The scraper is looping through Gender → School → Wrestler → Results.
                This process may take several hours to complete all Ohio high school wrestlers.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}