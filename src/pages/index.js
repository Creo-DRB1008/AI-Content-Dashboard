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
    { id: 'twitter', name: 'Twitter' },
    { id: 'linkedin', name: 'LinkedIn' },
    { id: 'rss', name: 'News' }
  ]

  // Make sure content is an array before filtering
  const filteredContent = Array.isArray(content) ? content : []

  return (
    <div className="container mx-auto px-4 py-8">
      <Head>
        <title>AI Content Aggregator</title>
        <meta name="description" content="Daily curated AI content" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">AI Content Aggregator</h1>
        <p className="text-gray-600">
          Your daily dose of AI news, research, and discussions
        </p>
      </header>

      <div className="flex flex-col md:flex-row md:justify-between md:items-start gap-4 mb-6">
        <CategoryTabs
          categories={categories}
          activeCategory={activeCategory}
          setActiveCategory={setActiveCategory}
        />

        <DatePicker
          selectedDate={selectedDate}
          onDateChange={setSelectedDate}
        />
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <p>Loading content...</p>
        </div>
      ) : filteredContent.length > 0 ? (
        <ContentList items={filteredContent} />
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-500">No content available for the selected filters</p>
          <button
            onClick={() => {
              setSelectedDate(null);
              setActiveCategory('all');
            }}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Reset Filters
          </button>
        </div>
      )}
    </div>
  )
}