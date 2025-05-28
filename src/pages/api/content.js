import { getPool, sql } from '../../lib/database'

export default async function handler(req, res) {
  try {
    // Get query parameters
    const { date, source, limit = 30 } = req.query

    // Get database connection
    const pool = await getPool()

    // Build SQL query with optional filters using correct column names
    let query = `
      SELECT TOP (@limit)
        id,
        title,
        content,
        summary,
        url,
        source,
        published_at,
        collected_at,
        author_name,
        author_url,
        likes,
        shares,
        comments,
        sentiment_score
      FROM content
      WHERE 1=1
    `

    const request = pool.request()
    request.input('limit', sql.Int, parseInt(limit))

    // Add date filter if provided
    if (date) {
      query += ` AND CAST(published_at AS DATE) = @date`
      request.input('date', sql.Date, new Date(date))
    }

    // Add source filter if provided
    if (source) {
      query += ` AND source = @source`
      request.input('source', sql.VarChar, source)
    }

    // Order by published date (most recent first)
    query += ` ORDER BY published_at DESC`

    // Execute query
    const result = await request.query(query)

    // Format the results
    const content = result.recordset.map(row => ({
      id: row.id,
      title: row.title,
      content: row.content,
      summary: row.summary,
      url: row.url,
      source: row.source,
      published_at: row.published_at,
      collected_at: row.collected_at,
      author_name: row.author_name,
      author_url: row.author_url,
      likes: row.likes,
      shares: row.shares,
      comments: row.comments,
      sentiment_score: row.sentiment_score
    }))

    // Return data from database
    res.status(200).json(content)
  } catch (error) {
    console.error('Error fetching content from database:', error)

    // Return error response
    res.status(500).json({
      error: 'Failed to fetch content from database',
      message: error.message
    })
  }
}