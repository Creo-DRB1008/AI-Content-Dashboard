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
    // Try to execute Python script to fetch available dates from database
    const { stdout } = await execPromise('python src/api/get_content.py --get-dates')
    const dates = JSON.parse(stdout)
    
    // Return real data from database
    res.status(200).json(dates)
  } catch (error) {
    console.error('Error fetching dates from database:', error)
    console.log('Falling back to mock dates')
    
    // Fall back to mock dates if database connection fails
    res.status(200).json(mockDates)
  }
}
