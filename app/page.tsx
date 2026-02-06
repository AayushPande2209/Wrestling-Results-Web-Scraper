import Link from 'next/link'
import ScraperControl from '../components/ScraperControl'
import { PerformanceChart } from '../components/PerformanceChart'
import { WinLossChart } from '../components/WinLossChart'
import { getAllWrestlersWithStats, getPerformanceOverTime } from '../utils/analytics'

export default async function HomePage() {
  // Get basic stats for the dashboard
  const wrestlers = await getAllWrestlersWithStats()
  const performanceData = await getPerformanceOverTime()
  
  const totalMatches = wrestlers.reduce((sum, wrestler) => sum + wrestler.total_matches, 0)
  const totalWins = wrestlers.reduce((sum, wrestler) => sum + wrestler.wins, 0)
  const totalLosses = wrestlers.reduce((sum, wrestler) => sum + wrestler.losses, 0)
  const overallWinRate = totalMatches > 0 ? ((totalWins / totalMatches) * 100).toFixed(1) : '0.0'

  return (
    <div className="px-4 py-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Wrestling Analytics Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">Ohio High School Wrestling Statistics</p>
      </div>

      {/* Scraper Control */}
      <div className="mb-8">
        <ScraperControl />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                <span className="text-white font-bold">🤼</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Wrestlers</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{wrestlers.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                <span className="text-white font-bold">🥊</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Matches</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{totalMatches}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                <span className="text-white font-bold">📊</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Win Rate</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{overallWinRate}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-red-500 rounded-md flex items-center justify-center">
                <span className="text-white font-bold">🏆</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Wins</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{totalWins}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      {wrestlers.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <PerformanceChart 
            data={performanceData} 
            title="Overall Performance Over Time"
          />
          <WinLossChart 
            wins={totalWins} 
            losses={totalLosses}
            title="Overall Win/Loss Breakdown"
          />
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Quick Actions</h2>
        <div className="flex flex-wrap gap-4">
          <Link 
            href="/wrestlers" 
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 font-medium transition-colors"
          >
            View All Wrestlers
          </Link>
          <Link 
            href="/teams" 
            className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 font-medium transition-colors"
          >
            Team Rankings
          </Link>
          <Link 
            href="/tournaments" 
            className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600 font-medium transition-colors"
          >
            Tournament Results
          </Link>
          <Link 
            href="/wrestlers" 
            className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 dark:bg-gray-500 dark:hover:bg-gray-600 font-medium transition-colors"
          >
            Search Wrestlers
          </Link>
        </div>
      </div>

      {/* Recent Activity or Top Performers */}
      {wrestlers.length > 0 && (
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Top Performers</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Wrestler</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Record</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Win %</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {wrestlers
                  .filter(w => w.total_matches > 0)
                  .sort((a, b) => b.win_percentage - a.win_percentage)
                  .slice(0, 5)
                  .map((wrestler) => (
                    <tr key={wrestler.wrestler_id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-4 py-2">
                        <Link 
                          href={`/wrestlers/${wrestler.wrestler_id}`}
                          className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
                        >
                          {wrestler.name}
                        </Link>
                      </td>
                      <td className="px-4 py-2 text-sm text-gray-900 dark:text-gray-100">
                        {wrestler.wins}-{wrestler.losses}
                      </td>
                      <td className="px-4 py-2 text-sm text-gray-900 dark:text-gray-100">
                        {wrestler.win_percentage}%
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {wrestlers.length === 0 && (
        <div className="mt-8 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <span className="text-yellow-600 dark:text-yellow-400 text-xl">⚠️</span>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800 dark:text-yellow-200">No Data Available</h3>
              <p className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                No wrestler data found. Use the "Run Scraper" button above to collect data from DubStat.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}