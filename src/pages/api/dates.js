import { getPool } from '../../lib/database'

export default async function handler(_, res) {
  try {
    // Get database connection
    const pool = await getPool()

    // Query to get available dates with content count
    const query = `
      SELECT
        CAST(published_at AS DATE) as date,
        COUNT(*) as count
      FROM content
      WHERE published_at IS NOT NULL
      GROUP BY CAST(published_at AS DATE)
      ORDER BY date DESC
    `

    const result = await pool.request().query(query)

    // Format the results
    const dates = result.recordset.map(row => ({
      date: row.date.toISOString().split('T')[0], // Format as YYYY-MM-DD
      count: row.count
    }))

    // Return data from database
    res.status(200).json(dates)
  } catch (error) {
    console.error('Error fetching dates from SQL Server database:', error)

    // Return error response
    res.status(500).json({
      error: 'Failed to fetch dates from SQL Server database',
      message: error.message
    })
  }
}
