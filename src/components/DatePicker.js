import { useState, useEffect, useRef } from 'react'

export default function DatePicker({ selectedDate, onDateChange }) {
  const [availableDates, setAvailableDates] = useState([])
  const [loading, setLoading] = useState(true)
  const [isExpanded, setIsExpanded] = useState(false)
  const dropdownRef = useRef(null)

  useEffect(() => {
    async function fetchDates() {
      try {
        setLoading(true)
        const res = await fetch('/api/dates')
        const data = await res.json()

        // Check if the response is an error or if data is an array
        if (res.ok && Array.isArray(data)) {
          setAvailableDates(data)
        } else {
          console.error('Error from dates API:', data)
          setAvailableDates([]) // Set empty array on error
        }
      } catch (error) {
        console.error('Error fetching dates:', error)
        setAvailableDates([]) // Set empty array on error
      } finally {
        setLoading(false)
      }
    }

    fetchDates()
  }, [])

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsExpanded(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
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

  const getSelectedDateLabel = () => {
    if (!selectedDate) return 'All Dates'
    const dateItem = availableDates.find(d => d.date === selectedDate)
    return dateItem ? `${formatDate(selectedDate)} (${dateItem.count})` : formatDate(selectedDate)
  }

  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2">
          <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span className="text-sm font-medium text-gray-700">Filter by Date:</span>
        </div>

        {loading ? (
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
            <span className="text-sm text-gray-500">Loading...</span>
          </div>
        ) : (
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="flex items-center space-x-2 px-3 py-2 bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 transition-colors duration-200"
            >
              <span className="text-sm font-medium text-gray-900">
                {getSelectedDateLabel()}
              </span>
              <svg
                className={`w-4 h-4 text-gray-500 transition-transform duration-200 ${
                  isExpanded ? 'rotate-180' : ''
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {/* Dropdown Menu */}
            {isExpanded && (
              <div className="absolute top-full left-0 mt-2 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-10 max-h-64 overflow-y-auto">
                <div className="p-2">
                  <button
                    onClick={() => {
                      handleDateChange(null)
                      setIsExpanded(false)
                    }}
                    className={`w-full px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 flex justify-between items-center ${
                      selectedDate === null
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <span>All Dates</span>
                    {selectedDate === null && (
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                  </button>

                  {availableDates.map((dateItem) => (
                    <button
                      key={dateItem.date}
                      onClick={() => {
                        handleDateChange(dateItem.date)
                        setIsExpanded(false)
                      }}
                      className={`w-full px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 flex justify-between items-center mt-1 ${
                        selectedDate === dateItem.date
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <span>{formatDate(dateItem.date)}</span>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs opacity-75">({dateItem.count})</span>
                        {selectedDate === dateItem.date && (
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        )}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Quick Date Actions */}
      <div className="hidden sm:flex items-center space-x-2">
        <button
          onClick={() => handleDateChange(null)}
          className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all duration-200 ${
            selectedDate === null
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
          }`}
        >
          All
        </button>
        {availableDates.slice(0, 3).map((dateItem) => (
          <button
            key={dateItem.date}
            onClick={() => handleDateChange(dateItem.date)}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all duration-200 ${
              selectedDate === dateItem.date
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
            }`}
          >
            {new Date(dateItem.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
          </button>
        ))}
      </div>
    </div>
  )
}
