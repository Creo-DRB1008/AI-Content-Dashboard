import { formatDistanceToNow } from 'date-fns'

export default function ContentCard({ item }) {
  const getSourceIcon = (source) => {
    switch(source) {
      case 'twitter':
        return '🐦'
      case 'linkedin':
        return '💼'
      case 'rss':
        return '📰'
      default:
        return '📄'
    }
  }
  
  return (
    <div className="border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
      <div className="p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-500">
            {getSourceIcon(item.source)} {item.source.charAt(0).toUpperCase() + item.source.slice(1)}
          </span>
          <span className="text-xs text-gray-400">
            {formatDistanceToNow(new Date(item.published_at), { addSuffix: true })}
          </span>
        </div>
        
        <h3 className="font-semibold mb-2 line-clamp-2">
          {item.title || 'Untitled'}
        </h3>
        
        <p className="text-sm text-gray-600 mb-4 line-clamp-3">
          {item.content || 'No content available'}
        </p>
        
        <a 
          href={item.url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          Read more →
        </a>
      </div>
    </div>
  )
}