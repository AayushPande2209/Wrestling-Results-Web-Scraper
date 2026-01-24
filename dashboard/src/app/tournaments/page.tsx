'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { getAllTournamentsWithStats } from '../../utils/analytics'
import type { TournamentStats } from '../../utils/analytics'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

export default function TournamentsPage() {
  const [tournaments, setTournaments] = useState<TournamentStats[]>([])
  const [loading, setLoading] = useState(true)
  const [sortBy, setSortBy] = useState<'date' | 'total_matches' | 'participating_teams'>('date')
  const [dateFilter, setDateFilter] = useState({
    startDate: '',
    endDate: ''
  })
  const [filteredTournaments, setFilteredTournaments] = useState<TournamentStats[]>([])

  useEffect(() => {
    async function fetchTournaments() {
      try {
        const data = await getAllTournamentsWithStats()
        setTournaments(data)
        setFilteredTournaments(data)
      } catch (error) {
        console.error('Error fetching tournaments:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchTournaments()
  }, [])

  useEffect(() => {
    let filtered = [...tournaments]

    // Apply date filtering
    if (dateFilter.startDate) {
      filtered = filtered.filter(tournament => {
        if (!tournament.date) return false
        return new Date(tournament.date) >= new Date(dateFilter.startDate)
      })
    }

    if (dateFilter.endDate) {
      filtered = filtered.filter(tournament => {
        if (!tournament.date) return false
        return new Date(tournament.date) <= new Date(dateFilter.endDate)
      })
    }

    setFilteredTournaments(filtered)
  }, [tournaments, dateFilter])

  const sortedTournaments = [...filteredTournaments].sort((a, b) => {
    switch (sortBy) {
      case 'date':
        if (!a.date && !b.date) return 0
        if (!a.date) return 1
        if (!b.date) return -1
        return new Date(b.date).getTime() - new Date(a.date).getTime()
      case 'total_matches':
        return b.total_matches - a.total_matches
      case 'participating_teams':
        return b.participating_teams - a.participating_teams
      default:
        return 0
    }
  })

  // Prepare chart data
  const matchTypesData = filteredTournaments.length > 0 ? [
    { name: 'Pins', value: filteredTournaments.reduce((sum, t) => sum + t.match_types.pins, 0) },
    { name: 'Decisions', value: filteredTournaments.reduce((sum, t) => sum + t.match_types.decisions, 0) },
    { name: 'Tech Falls', value: filteredTournaments.reduce((sum, t) => sum + t.match_types.tech_falls, 0) },
    { name: 'Major Decisions', value: filteredTournaments.reduce((sum, t) => sum + t.match_types.major_decisions, 0) }
  ].filter(item => item.value > 0) : []

  const tournamentComparisonData = filteredTournaments.slice(0, 10).map(t => ({
    name: t.name.length > 15 ? t.name.substring(0, 15) + '...' : t.name,
    matches: t.total_matches,
    teams: t.participating_teams
  }))

  if (loading) {
    return (
      <div className="px-4">
        <div className="text-center py-8">
          <div className="text-gray-500 dark:text-gray-400">Loading tournaments...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="px-4 py-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Tournaments</h1>
        <p className="text-gray-600 dark:text-gray-400">Tournament results and statistics</p>
      </div>

      {tournaments.length === 0 ? (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <span className="text-yellow-600 dark:text-yellow-400 text-xl">⚠️</span>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800 dark:text-yellow-200">No Tournament Data Available</h3>
              <p className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                No tournament data found. Make sure match data has been scraped from DubStat.
              </p>
            </div>
          </div>
        </div>
      ) : (
        <>
          {/* Date Range Filter */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Filter Tournaments</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Start Date</label>
                <input
                  type="date"
                  value={dateFilter.startDate}
                  onChange={(e) => setDateFilter(prev => ({ ...prev, startDate: e.target.value }))}
                  className="input w-full text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">End Date</label>
                <input
                  type="date"
                  value={dateFilter.endDate}
                  onChange={(e) => setDateFilter(prev => ({ ...prev, endDate: e.target.value }))}
                  className="input w-full text-sm"
                />
              </div>
              <div className="flex items-end">
                <button
                  onClick={() => setDateFilter({ startDate: '', endDate: '' })}
                  className="px-4 py-2 text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
                >
                  Clear Dates
                </button>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              Showing {filteredTournaments.length} of {tournaments.length} tournaments
            </div>
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                    <span className="text-white font-bold">🏆</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Tournaments</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{filteredTournaments.length}</p>
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
                  <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                    {filteredTournaments.reduce((sum, t) => sum + t.total_matches, 0)}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                    <span className="text-white font-bold">📌</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Pins</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                    {filteredTournaments.reduce((sum, t) => sum + t.match_types.pins, 0)}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-purple-500 rounded-md flex items-center justify-center">
                    <span className="text-white font-bold">👥</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Avg Teams/Tournament</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                    {filteredTournaments.length > 0 
                      ? Math.round(filteredTournaments.reduce((sum, t) => sum + t.participating_teams, 0) / filteredTournaments.length)
                      : 0
                    }
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* Tournament Comparison Chart */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Tournament Size Comparison</h2>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={tournamentComparisonData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="name" 
                      angle={-45}
                      textAnchor="end"
                      height={80}
                      fontSize={12}
                    />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="matches" fill="#10B981" name="Matches" />
                    <Bar dataKey="teams" fill="#6366F1" name="Teams" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Match Types Distribution */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Match Types Distribution</h2>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={matchTypesData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={(entry: any) => `${entry.name}: ${(entry.percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {matchTypesData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Tournaments Table */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Tournament List</h2>
              <div className="flex items-center space-x-2">
                <label className="text-sm text-gray-600 dark:text-gray-400">Sort by:</label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="select text-sm"
                >
                  <option value="date">Date</option>
                  <option value="total_matches">Matches</option>
                  <option value="participating_teams">Teams</option>
                </select>
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Tournament Name</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Date</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Matches</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Teams</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Pins</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {sortedTournaments.map((tournament) => (
                    <tr key={tournament.tournament_id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-4 py-2">
                        <div className="font-medium text-gray-900 dark:text-gray-100">{tournament.name}</div>
                      </td>
                      <td className="px-4 py-2 text-sm text-gray-900 dark:text-gray-100">
                        {tournament.date 
                          ? new Date(tournament.date).toLocaleDateString()
                          : 'N/A'
                        }
                      </td>
                      <td className="px-4 py-2 text-sm text-gray-900 dark:text-gray-100">
                        {tournament.total_matches}
                      </td>
                      <td className="px-4 py-2 text-sm text-gray-900 dark:text-gray-100">
                        {tournament.participating_teams}
                      </td>
                      <td className="px-4 py-2 text-sm font-medium text-green-600 dark:text-green-400">
                        {tournament.match_types.pins}
                      </td>
                      <td className="px-4 py-2">
                        <Link
                          href={`/tournaments/${tournament.tournament_id}`}
                          className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium"
                        >
                          View Details
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  )
}