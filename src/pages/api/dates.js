import { exec } from 'child_process'
import { promisify } from 'util'

const execPromise = promisify(exec)

// Mock dates as fallback if database connection fails
const mockDates = [
  { date: new Date().toISOString().split('T')[0], count: 6 },
  { date: new Date(Date.now() - 86400000).toISOString().split('T')[0], count: 4 },
  { date: new Date(Date.now() - 86400000 * 2).toISOString().split('T')[0], count: 8 },
  { date: new Date(Date.now() - 86400000 * 3).toISOString().split('T')[0], count: 5 },
  { date: new Date(Date.now() - 86400000 * 4).toISOString().split('T')[0], count: 3 },
  { date: new Date(Date.now() - 86400000 * 5).toISOString().split('T')[0], count: 7 },
  { date: new Date(Date.now() - 86400000 * 6).toISOString().split('T')[0], count: 2 },
]

export default async function handler(_, res) {
  try {
    // Execute Python script to fetch available dates from SQL Server database
    const { stdout } = await execPromise('python backend/api/get_content.py --get-dates')
    const dates = JSON.parse(stdout)
    
    // Return data from SQL Server database
    res.status(200).json(dates)
  } catch (error) {
    console.error('Error fetching dates from SQL Server database:', error)
    
    // Return error response instead of fallback
    res.status(500).json({ 
      error: 'Failed to fetch dates from SQL Server database',
      message: error.message 
    })
  }
}
