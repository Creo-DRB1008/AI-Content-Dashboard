import ContentCard from './ContentCard'

export default function ContentList({ items, onCardClick }) {
  // Check if items exists and is an array before accessing length
  if (!items || !Array.isArray(items) || items.length === 0) {
    return (
      <div className="text-center py-16">
        <div className="max-w-md mx-auto">
          <div className="w-16 h-16 mx-auto mb-4 text-gray-300">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" className="w-full h-full">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No content available</h3>
          <p className="text-gray-500 text-sm">
            Try adjusting your filters or check back later for new content.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Content count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-600">
          Showing {items.length} article{items.length !== 1 ? 's' : ''}
        </p>
      </div>

      {/* Responsive grid */}
      <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {items.map(item => (
          <ContentCard
            key={item.id}
            item={item}
            onClick={onCardClick}
          />
        ))}
      </div>
    </div>
  )
}