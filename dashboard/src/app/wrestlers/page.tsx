'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'

interface WrestlerStats {
  wrestler_id: string
  name: string
  weight_class: number | null
  wins: number
  losses: number
  win_percentage: number
  total_matches: number
}

export default function WrestlersPage() {
  const [wrestlers, setWrestlers] = useState<WrestlerStats[]>([])
  const [filteredWrestlers, setFilteredWrestlers] = useState<WrestlerStats[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchWrestlers() {
      try {
        const response = await fetch('/api/wrestlers')
        const data = await response.json()
        setWrestlers(data)
        setFilteredWrestlers(data)
      } catch (error) {
        console.error('Error fetching wrestlers:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchWrestlers()
  }, [])

  useEffect(() => {
    const filtered = wrestlers.filter(wrestler =>
      wrestler.name.toLowerCase().includes(searchTerm.toLowerCase())
    )
    setFilteredWrestlers(filtered)
  }, [searchTerm, wrestlers])

  if (loading) {
    return (
      <div className="px-4">
        <div className="text-center py-8">
          <div className="text-gray-500">Loading wrestlers...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="px-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Wrestlers</h1>
        <p className="text-gray-600">Click on a wrestler to view their profile</p>
      </div>

      <div className="mb-4">
        <input
          type="text"
          placeholder="Search wrestlers by name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="table">
            <thead className="bg-gray-50">
              <tr>
                <th>Name</th>
                <th>Weight Class</th>
                <th>Wins</th>
                <th>Losses</th>
                <th>Win %</th>
                <th>Total Matches</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredWrestlers.map((wrestler) => (
                <tr key={wrestler.wrestler_id} className="hover:bg-gray-50 cursor-pointer">
                  <td>
                    <Link 
                      href={`/wrestlers/${wrestler.wrestler_id}`}
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      {wrestler.name}
                    </Link>
                  </td>
                  <td>{wrestler.weight_class || 'N/A'}</td>
                  <td className="font-medium text-green-600">{wrestler.wins}</td>
                  <td className="font-medium text-red-600">{wrestler.losses}</td>
                  <td className="font-medium">{wrestler.win_percentage}%</td>
                  <td>{wrestler.total_matches}</td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {filteredWrestlers.length === 0 && wrestlers.length > 0 && (
            <div className="text-center py-8 text-gray-500">
              No wrestlers found matching "{searchTerm}".
            </div>
          )}
          
          {wrestlers.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No wrestlers found. Make sure data has been scraped and loaded.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}