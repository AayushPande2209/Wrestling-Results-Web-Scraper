import Link from 'next/link'
import { notFound } from 'next/navigation'
import { PerformanceChart } from '../../../components/PerformanceChart'
import { WinLossChart } from '../../../components/WinLossChart'
import { WinTypesChart } from '../../../components/WinTypesChart'
import { calculateWrestlerStats, getWrestlerMatches, getPerformanceOverTime, getWinTypesData } from '../../../utils/analytics'
import type { Match } from '../../../types/database'

interface WrestlerProfilePageProps {
  params: Promise<{
    id: string
  }>
}

function formatMatchType(matchType: string): string {
  switch (matchType) {
    case 'pin':
      return 'Pin'
    case 'decision':
      return 'Decision'
    case 'major_decision':
      return 'Major Decision'
    case 'tech_fall':
      return 'Tech Fall'
    case 'forfeit':
      return 'Forfeit'
    case 'disqualification':
      return 'Disqualification'
    default:
      return matchType
  }
}

function getMatchResult(match: Match, wrestlerId: string): { result: string; score: string } {
  const isWrestler1 = match.wrestler1_id === wrestlerId
  const isWinner = match.winner_id === wrestlerId
  
  const result = isWinner ? 'W' : 'L'
  
  // For pin matches, show only the pin time; for other matches, show scores
  const score = match.match_type === 'pin' && match.match_time
    ? match.match_time
    : isWrestler1 
      ? `${match.wrestler1_score}-${match.wrestler2_score}`
      : `${match.wrestler2_score}-${match.wrestler1_score}`
    
  return { result, score }
}

function getOpponentName(match: Match, wrestlerId: string): string {
  if (match.wrestler1_id === wrestlerId) {
    return match.wrestler2?.name || 'Unknown'
  } else {
    return match.wrestler1?.name || 'Unknown'
  }
}

export default async function WrestlerProfilePage({ params }: WrestlerProfilePageProps) {
  const { id } = await params
  
  // Get wrestler stats and matches
  const [stats, matches, performanceData, winTypesData] = await Promise.all([
    calculateWrestlerStats(id),
    getWrestlerMatches(id),
    getPerformanceOverTime(id),
    getWinTypesData(id)
  ])

  if (!stats) {
    notFound()
  }

  return (
    <div className="px-4">
      {/* Back link */}
      <div className="mb-6">
        <Link 
          href="/wrestlers" 
          className="text-blue-600 hover:text-blue-800 text-sm"
        >
          ← Back to Wrestlers
        </Link>
      </div>

      {/* Wrestler Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {stats.name}
        </h1>
        <div className="text-lg text-gray-600">
          {stats.weight_class ? `${stats.weight_class} lbs` : 'Weight class not specified'}
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card text-center">
          <div className="text-3xl font-bold text-green-600 mb-2">
            {stats.wins}
          </div>
          <div className="text-sm text-gray-600">Wins</div>
        </div>
        
        <div className="card text-center">
          <div className="text-3xl font-bold text-red-600 mb-2">
            {stats.losses}
          </div>
          <div className="text-sm text-gray-600">Losses</div>
        </div>
        
        <div className="card text-center">
          <div className="text-3xl font-bold text-blue-600 mb-2">
            {stats.win_percentage}%
          </div>
          <div className="text-sm text-gray-600">Win Percentage</div>
        </div>
        
        <div className="card text-center">
          <div className="text-3xl font-bold text-gray-900 mb-2">
            {stats.total_matches}
          </div>
          <div className="text-sm text-gray-600">Total Matches</div>
        </div>
      </div>

      {/* Charts Section */}
      {stats.total_matches > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <PerformanceChart 
            data={performanceData} 
            title={`${stats.name} - Performance Over Time`}
          />
          <WinLossChart 
            wins={stats.wins} 
            losses={stats.losses}
            title={`${stats.name} - Win/Loss Breakdown`}
          />
        </div>
      )}

      {stats.total_matches > 0 && (
        <div className="mb-8">
          <WinTypesChart 
            data={winTypesData}
            title={`${stats.name} - Win Types Distribution`}
          />
        </div>
      )}

      {/* Match Type Breakdown */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Match Type Breakdown (Wins Only)
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900 mb-1">
              {stats.pins}
            </div>
            <div className="text-sm text-gray-600">Pins</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900 mb-1">
              {stats.decisions}
            </div>
            <div className="text-sm text-gray-600">Decisions</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900 mb-1">
              {stats.tech_falls}
            </div>
            <div className="text-sm text-gray-600">Tech Falls</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900 mb-1">
              {stats.major_decisions}
            </div>
            <div className="text-sm text-gray-600">Major Decisions</div>
          </div>
        </div>
      </div>

      {/* Match History */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Recent Match History
        </h2>
        
        {matches.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="table">
              <thead className="bg-gray-50">
                <tr>
                  <th>Result</th>
                  <th>Opponent</th>
                  <th>Score</th>
                  <th>Match Type</th>
                  <th>Tournament</th>
                  <th>Round</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {matches.map((match) => {
                  const { result, score } = getMatchResult(match, id)
                  const opponent = getOpponentName(match, id)
                  
                  return (
                    <tr key={match.id}>
                      <td>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          result === 'W' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {result}
                        </span>
                      </td>
                      <td className="font-medium">{opponent}</td>
                      <td>{score}</td>
                      <td>{formatMatchType(match.match_type)}</td>
                      <td>{match.tournament?.name || 'N/A'}</td>
                      <td>{match.round || 'N/A'}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            No matches found for this wrestler.
          </div>
        )}
      </div>
    </div>
  )
}
