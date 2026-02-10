'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'
import { getTournamentDetails } from '../../../utils/analytics'
import type { TournamentDetails } from '../../../utils/analytics'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

export default function TournamentDetailPage() {
  const params = useParams()
  const tournamentId = params.id as string
  const [tournament, setTournament] = useState<TournamentDetails | null>(null)
  const [loading, setLoading] = useState(true)
  const [filterRound, setFilterRound] = useState<string>('all')

  useEffect(() => {
    async function fetchTournament() {
      if (!tournamentId) return
      
      try {
        const data = await getTournamentDetails(tournamentId)
        setTournament(data)
      } catch (error) {
        console.error('Error fetching tournament details:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchTournament()
  }, [tournamentId])

  if (loading) {
    return (
      <div className="px-4">
        <div className="text-center py-8">
          <div className="text-gray-500">Loading tournament details...</div>
        </div>
      </div>
    )
  }

  if (!tournament) {
    return (
      <div className="px-4">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <span className="text-red-600 text-xl">❌</span>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Tournament Not Found</h3>
              <p className="text-sm text-red-700 mt-1">
                The requested tournament could not be found.
              </p>
              <div className="mt-3">
                <Link
                  href="/tournaments"
                  className="text-red-600 hover:text-red-800 text-sm font-medium"
                >
                  ← Back to Tournaments
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Prepare chart data
  const matchTypesData = [
    { name: 'Pins', value: tournament.match_types.pins },
    { name: 'Decisions', value: tournament.match_types.decisions },
    { name: 'Tech Falls', value: tournament.match_types.tech_falls },
    { name: 'Major Decisions', value: tournament.match_types.major_decisions }
  ].filter(item => item.value > 0)

  // Get unique rounds for filtering
  const rounds = ['all', ...Array.from(new Set(tournament.matches.map(m => m.round))).sort()]
  
  // Filter matches by round
  const filteredMatches = filterRound === 'all' 
    ? tournament.matches 
    : tournament.matches.filter(m => m.round === filterRound)

  // Team performance data
  const teamPerformance: { [team: string]: { wins: number; matches: number } } = {}
  
  tournament.matches.forEach(match => {
    // Extract team names (using same logic as teams page)
    const team1 = extractTeamFromWrestlerName(match.wrestler1_name)
    const team2 = extractTeamFromWrestlerName(match.wrestler2_name)
    
    // Initialize teams
    if (!teamPerformance[team1]) teamPerformance[team1] = { wins: 0, matches: 0 }
    if (!teamPerformance[team2]) teamPerformance[team2] = { wins: 0, matches: 0 }
    
    // Count matches
    teamPerformance[team1].matches++
    teamPerformance[team2].matches++
    
    // Count wins
    if (match.winner_name === match.wrestler1_name) {
      teamPerformance[team1].wins++
    } else if (match.winner_name === match.wrestler2_name) {
      teamPerformance[team2].wins++
    }
  })

  const teamPerformanceData = Object.entries(teamPerformance).map(([team, stats]) => ({
    team,
    wins: stats.wins,
    matches: stats.matches,
    winRate: stats.matches > 0 ? Math.round((stats.wins / stats.matches) * 100) : 0
  })).sort((a, b) => b.winRate - a.winRate)

  // Helper function to extract team name (same as in analytics.ts)
  function extractTeamFromWrestlerName(wrestlerName: string): string {
    const parenMatch = wrestlerName.match(/\(([^)]+)\)$/)
    if (parenMatch) return parenMatch[1].trim()
    
    const dashMatch = wrestlerName.match(/\s-\s(.+)$/)
    if (dashMatch) return dashMatch[1].trim()
    
    const firstLetter = wrestlerName.charAt(0).toUpperCase()
    return `Team ${firstLetter}`
  }

  return (
    <div className="px-4 py-6">
      {/* Header */}
      <div className="mb-6">
        <Link
          href="/tournaments"
          className="text-blue-600 hover:text-blue-800 text-sm font-medium mb-2 inline-block"
        >
          ← Back to Tournaments
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">{tournament.name}</h1>
        <p className="text-gray-600">
          {tournament.date 
            ? `Tournament held on ${new Date(tournament.date).toLocaleDateString()}`
            : 'Tournament details'
          }
        </p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                <span className="text-white font-bold">🥊</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Matches</p>
              <p className="text-2xl font-bold text-gray-900">{tournament.total_matches}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                <span className="text-white font-bold">👥</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Teams</p>
              <p className="text-2xl font-bold text-gray-900">{tournament.participating_teams}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                <span className="text-white font-bold">📌</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Pins</p>
              <p className="text-2xl font-bold text-gray-900">{tournament.match_types.pins}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-purple-500 rounded-md flex items-center justify-center">
                <span className="text-white font-bold">⚡</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Tech Falls</p>
              <p className="text-2xl font-bold text-gray-900">{tournament.match_types.tech_falls}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Match Types Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Match Types</h2>
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

        {/* Team Performance Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Team Performance</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={teamPerformanceData.slice(0, 8)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="team" 
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  fontSize={12}
                />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => [
                    value, 
                    name === 'wins' ? 'Wins' : name === 'matches' ? 'Matches' : 'Win Rate %'
                  ]}
                />
                <Bar dataKey="wins" fill="#10B981" name="wins" />
                <Bar dataKey="winRate" fill="#6366F1" name="winRate" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Matches Table */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Match Results</h2>
          <div className="flex items-center space-x-2">
            <label className="text-sm text-gray-600">Filter by round:</label>
            <select
              value={filterRound}
              onChange={(e) => setFilterRound(e.target.value)}
              className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {rounds.map(round => (
                <option key={round} value={round}>
                  {round === 'all' ? 'All Rounds' : round}
                </option>
              ))}
            </select>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Wrestler 1</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Wrestler 2</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Score</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Winner</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Match Type</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Round</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredMatches.map((match) => (
                <tr key={match.id} className="hover:bg-gray-50">
                  <td className="px-4 py-2">
                    <div className={`font-medium ${match.winner_name === match.wrestler1_name ? 'text-green-600' : 'text-gray-900'}`}>
                      {match.wrestler1_name}
                    </div>
                  </td>
                  <td className="px-4 py-2">
                    <div className={`font-medium ${match.winner_name === match.wrestler2_name ? 'text-green-600' : 'text-gray-900'}`}>
                      {match.wrestler2_name}
                    </div>
                  </td>
                  <td className="px-4 py-2 text-sm text-gray-900">
                    {match.match_type === 'pin' && match.match_time
                      ? match.match_time
                      : `${match.wrestler1_score} - ${match.wrestler2_score}`
                    }
                  </td>
                  <td className="px-4 py-2">
                    <div className="text-sm font-medium text-green-600">
                      {match.winner_name || 'No Contest'}
                    </div>
                  </td>
                  <td className="px-4 py-2">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      match.match_type === 'pin' ? 'bg-red-100 text-red-800' :
                      match.match_type === 'tech_fall' ? 'bg-orange-100 text-orange-800' :
                      match.match_type === 'major_decision' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {match.match_type.replace('_', ' ').toUpperCase()}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-sm text-gray-900">
                    {match.round}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {filteredMatches.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No matches found for the selected round.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
