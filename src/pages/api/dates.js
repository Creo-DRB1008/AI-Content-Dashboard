export default async function handler(_, res) {
  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:3000'
    const url = `${backendUrl}/api/content/dates`

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

    const dates = await response.json()

    // Return data from backend
    res.status(200).json(dates)
  } catch (error) {
    console.error('Error fetching dates from backend:', error)

    // Return error response
    res.status(500).json({
      error: 'Failed to fetch dates from backend',
      message: error.message
    })
  }
}
