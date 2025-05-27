import { useState, useEffect } from 'react'

export default function DatePicker({ selectedDate, onDateChange }) {
  const [availableDates, setAvailableDates] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchDates() {
      try {
        setLoading(true)
        const res = await fetch('/api/dates')
        const data = await res.json()
        setAvailableDates(data)
      } catch (error) {
        console.error('Error fetching dates:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchDates()
  }, [])

  const handleDateChange = (date) => {
    onDateChange(date)
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    })
  }

  return (
    <div className="mb-6">
      <h2 className="text-lg font-semibold mb-3 text-gray-900">Filter by Date</h2>

      {loading ? (
        <div className="flex items-center space-x-2">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
          <span className="text-sm text-gray-500">Loading dates...</span>
        </div>
      ) : (
        <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
          <button
            onClick={() => handleDateChange(null)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
              selectedDate === null
                ? 'bg-blue-500 text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:shadow-sm'
            }`}
          >
            All Dates
          </button>

          {availableDates.map((dateItem) => (
            <button
              key={dateItem.date}
              onClick={() => handleDateChange(dateItem.date)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                selectedDate === dateItem.date
                  ? 'bg-blue-500 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:shadow-sm'
              }`}
            >
              <span className="hidden sm:inline">{formatDate(dateItem.date)}</span>
              <span className="sm:hidden">{new Date(dateItem.date).getDate()}</span>
              <span className="ml-1 text-xs opacity-75">({dateItem.count})</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
