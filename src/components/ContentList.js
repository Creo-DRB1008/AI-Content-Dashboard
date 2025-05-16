import ContentCard from './ContentCard'

export default function ContentList({ items }) {
  // Check if items exists and is an array before accessing length
  if (!items || !Array.isArray(items) || items.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No content available</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {items.map(item => (
        <ContentCard key={item.id} item={item} />
      ))}
    </div>
  )
}