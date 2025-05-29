export default async function handler(req, res) {
  try {
    // Get query parameters
    const { date, source, limit = 30 } = req.query

    // Build query string for backend API
    const params = new URLSearchParams()
    if (date) params.append('date', date)
    if (source) params.append('source', source)
    if (limit) params.append('limit', limit)

    const queryString = params.toString()
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:3000'
    const url = `${backendUrl}/api/content${queryString ? `?${queryString}` : ''}`

    // Call backend API
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status} ${response.statusText}`)
    }

    const content = await response.json()

    // Return data from backend
    res.status(200).json(content)
  } catch (error) {
    console.error('Error fetching content from backend:', error)

    // Return error response
    res.status(500).json({
      error: 'Failed to fetch content from backend',
      message: error.message
    })
  }
}