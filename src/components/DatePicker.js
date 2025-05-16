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
      <h2 className="text-lg font-semibold mb-2">Filter by Date</h2>
      
      {loading ? (
        <div className="text-sm text-gray-500">Loading dates...</div>
      ) : (
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => handleDateChange(null)}
            className={`px-3 py-1 rounded-full text-sm ${
              selectedDate === null
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 hover:bg-gray-300'
            }`}
          >
            All Dates
          </button>
          
          {availableDates.map((dateItem) => (
            <button
              key={dateItem.date}
              onClick={() => handleDateChange(dateItem.date)}
              className={`px-3 py-1 rounded-full text-sm ${
                selectedDate === dateItem.date
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 hover:bg-gray-300'
              }`}
            >
              {formatDate(dateItem.date)} 
              <span className="ml-1 text-xs">({dateItem.count})</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
