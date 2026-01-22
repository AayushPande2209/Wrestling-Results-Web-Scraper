import { NextResponse } from 'next/server'
import { getAllWrestlersWithStats } from '../../../utils/analytics'

export async function GET() {
  try {
    const wrestlers = await getAllWrestlersWithStats()
    return NextResponse.json(wrestlers)
  } catch (error) {
    console.error('Error fetching wrestlers:', error)
    return NextResponse.json(
      { error: 'Failed to fetch wrestlers' },
      { status: 500 }
    )
  }
}