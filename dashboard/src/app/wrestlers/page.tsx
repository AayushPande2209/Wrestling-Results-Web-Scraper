import Link from 'next/link'
import { getAllWrestlersWithStats } from '../../utils/analytics'

export default async function WrestlersPage() {
  const wrestlers = await getAllWrestlersWithStats()

  return (
    <div className="px-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Wrestlers</h1>
        <p className="text-gray-600">Click on a wrestler to view their profile</p>
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
              {wrestlers.map((wrestler) => (
                <tr key={wrestler.wrestler_id} className="hover:bg-gray-50">
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