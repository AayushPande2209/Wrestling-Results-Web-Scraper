'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { getAllWrestlersWithStats, getUniqueTeams, getUniqueWeightClasses } from '../../utils/analytics'

interface WrestlerStats {
  wrestler_id: string
  name: string
  weight_class: number | null
  wins: number
  losses: number
  win_percentage: number
  total_matches: number
}

interface FilterState {
  searchTerm: string
  team: string
  weightClass: string
  minMatches: number
  sortBy: 'name' | 'win_percentage' | 'total_wins' | 'total_matches'
  sortOrder: 'asc' | 'desc'
}

export default function WrestlersPage() {
  const [wrestlers, setWrestlers] = useState<WrestlerStats[]>([])
  const [filteredWrestlers, setFilteredWrestlers] = useState<WrestlerStats[]>([])
  const [teams, setTeams] = useState<string[]>([])
  const [weightClasses, setWeightClasses] = useState<number[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState<FilterState>({
    searchTerm: '',
    team: 'all',
    weightClass: 'all',
    minMatches: 0,
    sortBy: 'win_percentage',
    sortOrder: 'desc'
  })

  useEffect(() => {
    async function fetchData() {
      try {
        const [wrestlersData, teamsData, weightClassesData] = await Promise.all([
          getAllWrestlersWithStats(),
          getUniqueTeams(),
          getUniqueWeightClasses()
        ])
        setWrestlers(wrestlersData)
        setTeams(teamsData)
        setWeightClasses(weightClassesData)
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [])

  useEffect(() => {
    let filtered = [...wrestlers]

    // Apply filters
    if (filters.searchTerm) {
      filtered = filtered.filter(wrestler =>
        wrestler.name.toLowerCase().includes(filters.searchTerm.toLowerCase())
      )
    }

    if (filters.team !== 'all') {
      filtered = filtered.filter(wrestler => {
        const wrestlerTeam = extractTeamFromWrestlerName(wrestler.name)
        return wrestlerTeam === filters.team
      })
    }

    if (filters.weightClass !== 'all') {
      const weightClass = parseInt(filters.weightClass)
      filtered = filtered.filter(wrestler => wrestler.weight_class === weightClass)
    }

    if (filters.minMatches > 0) {
      filtered = filtered.filter(wrestler => wrestler.total_matches >= filters.minMatches)
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aValue: any, bValue: any
      
      switch (filters.sortBy) {
        case 'name':
          aValue = a.name.toLowerCase()
          bValue = b.name.toLowerCase()
          break
        case 'win_percentage':
          aValue = a.win_percentage
          bValue = b.win_percentage
          break
        case 'total_wins':
          aValue = a.wins
          bValue = b.wins
          break
        case 'total_matches':
          aValue = a.total_matches
          bValue = b.total_matches
          break
        default:
          return 0
      }

      if (filters.sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1
      } else {
        return aValue < bValue ? 1 : -1
      }
    })

    setFilteredWrestlers(filtered)
  }, [filters, wrestlers])

  // Helper function to extract team name (same as in analytics.ts)
  function extractTeamFromWrestlerName(wrestlerName: string): string {
    const parenMatch = wrestlerName.match(/\(([^)]+)\)$/)
    if (parenMatch) return parenMatch[1].trim()
    
    const dashMatch = wrestlerName.match(/\s-\s(.+)$/)
    if (dashMatch) return dashMatch[1].trim()
    
    const firstLetter = wrestlerName.charAt(0).toUpperCase()
    return `Team ${firstLetter}`
  }

  const handleFilterChange = (key: keyof FilterState, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  const clearFilters = () => {
    setFilters({
      searchTerm: '',
      team: 'all',
      weightClass: 'all',
      minMatches: 0,
      sortBy: 'win_percentage',
      sortOrder: 'desc'
    })
  }

  if (loading) {
    return (
      <div className="px-4">
        <div className="text-center py-8">
          <div className="text-gray-500 dark:text-gray-400">Loading wrestlers...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="px-4 py-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Wrestlers</h1>
        <p className="text-gray-600 dark:text-gray-400">Click on a wrestler to view their profile</p>
      </div>

      {/* Enhanced Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6 border border-gray-200 dark:border-gray-700">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Filters & Search</h2>
          <button
            onClick={clearFilters}
            className="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
          >
            Clear All Filters
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Search Name</label>
            <input
              type="text"
              placeholder="Search wrestlers..."
              value={filters.searchTerm}
              onChange={(e) => handleFilterChange('searchTerm', e.target.value)}
              className="w-full input text-sm"
            />
          </div>

          {/* Team Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Team</label>
            <select
              value={filters.team}
              onChange={(e) => handleFilterChange('team', e.target.value)}
              className="w-full select text-sm"
            >
              <option value="all">All Teams</option>
              {teams.map(team => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </div>

          {/* Weight Class Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Weight Class</label>
            <select
              value={filters.weightClass}
              onChange={(e) => handleFilterChange('weightClass', e.target.value)}
              className="w-full select text-sm"
            >
              <option value="all">All Weights</option>
              {weightClasses.map(weight => (
                <option key={weight} value={weight.toString()}>{weight} lbs</option>
              ))}
            </select>
          </div>

          {/* Minimum Matches */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Min Matches</label>
            <input
              type="number"
              min="0"
              value={filters.minMatches}
              onChange={(e) => handleFilterChange('minMatches', parseInt(e.target.value) || 0)}
              className="w-full input text-sm"
            />
          </div>

          {/* Sort By */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Sort By</label>
            <select
              value={filters.sortBy}
              onChange={(e) => handleFilterChange('sortBy', e.target.value)}
              className="w-full select text-sm"
            >
              <option value="win_percentage">Win %</option>
              <option value="total_wins">Total Wins</option>
              <option value="total_matches">Total Matches</option>
              <option value="name">Name</option>
            </select>
          </div>

          {/* Sort Order */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Order</label>
            <select
              value={filters.sortOrder}
              onChange={(e) => handleFilterChange('sortOrder', e.target.value)}
              className="w-full select text-sm"
            >
              <option value="desc">High to Low</option>
              <option value="asc">Low to High</option>
            </select>
          </div>
        </div>

        {/* Results Summary */}
        <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">
          Showing {filteredWrestlers.length} of {wrestlers.length} wrestlers
        </div>
      </div>

      {/* Results Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Name</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Team</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Weight Class</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Record</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Win %</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-400">Total Matches</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {filteredWrestlers.map((wrestler) => (
                <tr key={wrestler.wrestler_id} className="hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer">
                  <td className="px-4 py-3">
                    <Link 
                      href={`/wrestlers/${wrestler.wrestler_id}`}
                      className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
                    >
                      {wrestler.name}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100">
                    {extractTeamFromWrestlerName(wrestler.name)}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100">
                    {wrestler.weight_class ? `${wrestler.weight_class} lbs` : 'N/A'}
                  </td>
                  <td className="px-4 py-3 text-sm">
                    <span className="font-medium text-green-600 dark:text-green-400">{wrestler.wins}</span>
                    <span className="text-gray-500 dark:text-gray-400"> - </span>
                    <span className="font-medium text-red-600 dark:text-red-400">{wrestler.losses}</span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center">
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100 mr-2">
                        {wrestler.win_percentage}%
                      </span>
                      <div className="w-16 bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                        <div
                          className="bg-blue-600 dark:bg-blue-400 h-2 rounded-full"
                          style={{ width: `${wrestler.win_percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100">
                    {wrestler.total_matches}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {filteredWrestlers.length === 0 && wrestlers.length > 0 && (
            <div className="text-center py-8 text-gray-500 dark:text-gray-400">
              No wrestlers found matching the current filters.
            </div>
          )}
          
          {wrestlers.length === 0 && (
            <div className="text-center py-8 text-gray-500 dark:text-gray-400">
              No wrestlers found. Make sure data has been scraped and loaded.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}