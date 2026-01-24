'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { getAllTeamsWithStats, getTeamComparisonData } from '../../utils/analytics'
import type { TeamStats, TeamComparisonData } from '../../utils/analytics'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF7C7C']

export default function TeamsPage() {
  const [teams, setTeams] = useState<TeamStats[]>([])
  const [comparisonData, setComparisonData] = useState<TeamComparisonData[]>([])
  const [loading, setLoading] = useState(true)
  const [sortBy, setSortBy] = useState<'win_percentage' | 'total_wins' | 'wrestler_count'>('win_percentage')

  useEffect(() => {
    async function fetchTeamData() {
      try {
        const [teamsData, compData] = await Promise.all([
          getAllTeamsWithStats(),
          getTeamComparisonData()
        ])
        setTeams(teamsData)
        setComparisonData(compData)
      } catch (error) {
        console.error('Error fetching team data:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchTeamData()
  }, [])

  const sortedTeams = [...teams].sort((a, b) => {
    switch (sortBy) {
      case 'win_percentage':
        return b.win_percentage - a.win_percentage
      case 'total_wins':
        return b.total_wins - a.total_wins
      case 'wrestler_count':
        return b.wrestler_count - a.wrestler_count
      default:
        return 0
    }
  })

  if (loading) {
    return (
      <div className="px-4">
        <div className="text-center py-8">
          <div className="text-gray-500 dark:text-gray-400">Loading teams...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="px-4 py-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Team Rankings</h1>
        <p className="text-gray-600 dark:text-gray-400">Team performance statistics and comparisons</p>
      </div>

      {teams.length === 0 ? (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <span className="text-yellow-600 dark:text-yellow-400 text-xl">⚠️</span>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800 dark:text-yellow-200">No Team Data Available</h3>
              <p className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                No team data found. Teams are derived from wrestler data. Make sure wrestler data has been scraped.
              </p>
            </div>
          </div>
        </div>
      ) : (
        <>
          {/* Team Comparison Chart */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Team Wins Comparison</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={comparisonData.slice(0, 10)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="team_name" 
                    angle={-45}
                    textAnchor="end"
                    height={80}
                    fontSize={12}
                  />
                  <YAxis />
                  <Tooltip 
                    formatter={(value, name) => [
                      value, 
                      name === 'wins' ? 'Total Wins' : 'Total Matches'
                    ]}
                  />
                  <Bar dataKey="wins" fill="#10B981" name="wins" />
                  <Bar dataKey="matches" fill="#6B7280" name="matches" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Win Percentage Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Win Percentage Distribution</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={teams.slice(0, 8)}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={(entry: any) => `${entry.team_name}: ${entry.win_percentage}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="win_percentage"
                  >
                    {teams.slice(0, 8).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value}%`, 'Win Percentage']} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Team Rankings Table */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Team Rankings</h2>
              <div className="flex items-center space-x-2">
                <label className="text-sm text-gray-600 dark:text-gray-400">Sort by:</label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="select text-sm"
                >
                  <option value="win_percentage">Win %</option>
                  <option value="total_wins">Total Wins</option>
                  <option value="wrestler_count">Wrestlers</option>
                </select>
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Rank</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Team Name</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Wrestlers</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Total Wins</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Win %</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Pins</th>
                    <th className="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Top Wrestler</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {sortedTeams.map((team, index) => (
                    <tr key={team.team_name} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-4 py-2 text-sm font-medium text-gray-900 dark:text-gray-100">
                        {index + 1}
                      </td>
                      <td className="px-4 py-2">
                        <div className="font-medium text-gray-900 dark:text-gray-100">{team.team_name}</div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          {team.total_wins}-{team.total_losses} record
                        </div>
                      </td>
                      <td className="px-4 py-2 text-sm text-gray-900 dark:text-gray-100">
                        {team.wrestler_count}
                      </td>
                      <td className="px-4 py-2 text-sm font-medium text-green-600 dark:text-green-400">
                        {team.total_wins}
                      </td>
                      <td className="px-4 py-2">
                        <div className="flex items-center">
                          <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                            {team.win_percentage}%
                          </div>
                          <div className="ml-2 w-16 bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                            <div
                              className="bg-blue-600 dark:bg-blue-400 h-2 rounded-full"
                              style={{ width: `${team.win_percentage}%` }}
                            ></div>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-2 text-sm text-gray-900 dark:text-gray-100">
                        {team.pins}
                      </td>
                      <td className="px-4 py-2 text-sm text-blue-600 dark:text-blue-400">
                        {team.top_wrestler}
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