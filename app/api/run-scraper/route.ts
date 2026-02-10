import { NextRequest, NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'

export async function POST(request: NextRequest) {
  try {
    console.log('🏆 Starting scraper from dashboard...')
    
    // Path to the scraper directory
    const scraperPath = path.join(process.cwd(), '..', 'scraper')
    const scriptPath = path.join(scraperPath, 'run_scraper.py')
    
    // Check if scraper exists
    const fs = require('fs')
    if (!fs.existsSync(scriptPath)) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Scraper script not found',
          path: scriptPath 
        },
        { status: 404 }
      )
    }
    
    // Return immediately with status - scraper runs in background
    // In production, you'd want to use a proper job queue
    const scraperProcess = spawn('python3', ['run_scraper.py'], {
      cwd: scraperPath,
      detached: true,
      stdio: 'ignore'
    })
    
    // Don't wait for the process to complete
    scraperProcess.unref()
    
    console.log(`🕷️ Scraper started with PID: ${scraperProcess.pid}`)
    
    return NextResponse.json({
      success: true,
      message: 'Scraper started successfully',
      pid: scraperProcess.pid,
      status: 'running',
      startTime: new Date().toISOString()
    })
    
  } catch (error) {
    console.error('❌ Error starting scraper:', error)
    
    return NextResponse.json(
      { 
        success: false, 
        error: 'Failed to start scraper',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}

export async function GET() {
  // Simple status endpoint
  return NextResponse.json({
    message: 'Scraper API is running',
    endpoints: {
      'POST /api/run-scraper': 'Start the scraper process'
    }
  })
}