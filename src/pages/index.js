import { useState, useEffect } from 'react'
import Head from 'next/head'
import ContentList from '../components/ContentList'
import CategoryTabs from '../components/CategoryTabs'
import DatePicker from '../components/DatePicker'

export default function Home() {
  const [content, setContent] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeCategory, setActiveCategory] = useState('all')
  const [selectedDate, setSelectedDate] = useState(null)

  useEffect(() => {
    async function fetchContent() {
      try {
        setLoading(true)

        // Build URL with query parameters
        let url = '/api/content'
        const params = new URLSearchParams()

        if (selectedDate) {
          params.append('date', selectedDate)
        }

        if (activeCategory !== 'all') {
          params.append('source', activeCategory)
        }

        // Add params to URL if any exist
        if (params.toString()) {
          url += `?${params.toString()}`
        }

        const res = await fetch(url)
        const data = await res.json()
        setContent(data)
      } catch (error) {
        console.error('Error fetching content:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchContent()
  }, [activeCategory, selectedDate])

  const categories = [
    { id: 'all', name: 'All' },
    // { id: 'twitter', name: 'Twitter' },     // Temporarily commented out
    // { id: 'linkedin', name: 'LinkedIn' },   // Temporarily commented out
    { id: 'rss', name: 'News' }
    // Future: YouTube will be added here
  ]

  // Make sure content is an array before filtering
  const filteredContent = Array.isArray(content) ? content : []

  const handleCardClick = (item) => {
    // Optional: Add analytics or custom behavior here
    console.log('Card clicked:', item.title)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>AI Content Aggregator</title>
        <meta name="description" content="Daily curated AI content with intelligent summaries" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {/* Header */}
        <header className="mb-8 sm:mb-12">
          <div className="text-center sm:text-left">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 mb-3 sm:mb-4">
              AI Content Aggregator
            </h1>
            <p className="text-gray-600 text-lg sm:text-xl max-w-2xl">
              Your daily dose of AI news, research, and discussions with intelligent summaries
            </p>
          </div>
        </header>

        {/* Filters Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sm:p-6 mb-6 sm:mb-8">
          <div className="flex flex-col lg:flex-row lg:justify-between lg:items-start gap-6">
            <div className="flex-1">
              <CategoryTabs
                categories={categories}
                activeCategory={activeCategory}
                setActiveCategory={setActiveCategory}
              />
            </div>

            <div className="lg:w-80">
              <DatePicker
                selectedDate={selectedDate}
                onDateChange={setSelectedDate}
              />
            </div>
          </div>
        </div>

        {/* Content Section */}
        <main>
          {loading ? (
            <div className="flex flex-col items-center justify-center py-16 sm:py-24">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
              <p className="text-gray-600 text-lg">Loading content...</p>
            </div>
          ) : filteredContent.length > 0 ? (
            <ContentList
              items={filteredContent}
              onCardClick={handleCardClick}
            />
          ) : (
            <div className="text-center py-16 sm:py-24">
              <div className="max-w-md mx-auto">
                <div className="w-20 h-20 mx-auto mb-6 text-gray-300">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" className="w-full h-full">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.291-1.007-5.824-2.709M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">No content available</h3>
                <p className="text-gray-500 mb-6">
                  No articles match your current filters. Try adjusting your selection or check back later for new content.
                </p>
                <button
                  onClick={() => {
                    setSelectedDate(null);
                    setActiveCategory('all');
                  }}
                  className="btn-primary"
                >
                  Reset Filters
                </button>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}