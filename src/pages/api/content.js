import { exec } from 'child_process'
import { promisify } from 'util'

const execPromise = promisify(exec)

export default async function handler(req, res) {
  try {
    // Get query parameters
    const { date, source, limit } = req.query

    // Build command with optional parameters
    let command = 'python backend/api/get_content.py'
    if (date) command += ` --date ${date}`
    if (source) command += ` --source ${source}`
    if (limit) command += ` --limit ${limit}`

    // Execute Python script to fetch content from database
    const { stdout } = await execPromise(command)
    const content = JSON.parse(stdout)

    // Return data from database
    res.status(200).json(content)
  } catch (error) {
    console.error('Error fetching content from database:', error)
    
    // Return error response instead of mock data
    res.status(500).json({ 
      error: 'Failed to fetch content from database',
      message: error.message 
    })
  }
}