import { useState } from 'react'
import { formatSmartDate, formatFullTimestamp } from '../utils/timeUtils'

export default function ContentCard({ item, onClick }) {
  const [imageError, setImageError] = useState(false)
  const [imageLoading, setImageLoading] = useState(true)

  const getSourceIcon = (source) => {
    switch(source) {
      // case 'twitter':        // Temporarily commented out
      //   return '🐦'          // Temporarily commented out
      // case 'linkedin':       // Temporarily commented out
      //   return '💼'          // Temporarily commented out
      case 'rss':
        return '📰'
      default:
        return '📄'
    }
  }

  const getSourceColor = (source) => {
    switch(source) {
      case 'rss':
        return 'bg-orange-100 text-orange-800'
      case 'twitter':
        return 'bg-blue-100 text-blue-800'
      case 'linkedin':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const handleCardClick = (e) => {
    // Don't trigger card click if clicking on the read more button
    if (e.target.closest('a')) return

    if (onClick) {
      onClick(item)
    } else {
      // Default behavior: open article in new tab
      window.open(item.url, '_blank', 'noopener,noreferrer')
    }
  }

  const handleImageLoad = () => {
    setImageLoading(false)
  }

  const handleImageError = () => {
    setImageError(true)
    setImageLoading(false)
  }

  // Extract image from content or use a placeholder
  const getImageUrl = () => {
    // Try to extract image from content
    if (item.content) {
      const imgMatch = item.content.match(/<img[^>]+src="([^">]+)"/i)
      if (imgMatch && imgMatch[1]) {
        return imgMatch[1]
      }
    }

    // Check if there's a direct image field
    if (item.image_url) {
      return item.image_url
    }

    return null
  }

  const imageUrl = getImageUrl()
  const hasValidImage = imageUrl && !imageError

  return (
    <article
      className="group bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm card-hover cursor-pointer"
      onClick={handleCardClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          handleCardClick(e)
        }
      }}
    >
      {/* Image Section */}
      {hasValidImage && (
        <div className="relative h-48 bg-gray-100 overflow-hidden">
          {imageLoading && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="animate-pulse bg-gray-200 w-full h-full"></div>
            </div>
          )}
          <img
            src={imageUrl}
            alt={item.title || 'Article image'}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onLoad={handleImageLoad}
            onError={handleImageError}
            loading="lazy"
          />
        </div>
      )}

      <div className="p-5">
        {/* Header with source and time */}
        <div className="flex items-center justify-between mb-3">
          <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${getSourceColor(item.source)}`}>
            <span className="mr-1">{getSourceIcon(item.source)}</span>
            {item.source.charAt(0).toUpperCase() + item.source.slice(1)}
          </span>
          <time
            className="text-xs text-gray-500 font-medium"
            dateTime={item.published_at}
            title={formatFullTimestamp(item.published_at)}
          >
            {formatSmartDate(item.published_at)}
          </time>
        </div>

        {/* Title */}
        <h3 className="font-bold text-gray-900 mb-3 line-clamp-2 text-lg leading-tight group-hover:text-blue-600 transition-colors duration-200">
          {item.title || 'Untitled'}
        </h3>

        {/* Summary/Content */}
        <div className="mb-4">
          {item.summary ? (
            <>
              <div className="inline-flex items-center text-xs text-blue-600 font-medium bg-blue-50 px-2 py-1 rounded-full mb-2">
                <span className="mr-1">✨</span>
                AI Summary
              </div>
              <p className="text-gray-700 text-sm leading-relaxed mb-2">
                {item.summary}
              </p>
            </>
          ) : (
            <p className="text-gray-600 text-sm leading-relaxed line-clamp-4 mb-2">
              {item.content || 'No content available'}
            </p>
          )}
        </div>

        {/* Author if available */}
        {item.author_name && (
          <div className="text-xs text-gray-500 mb-3">
            By {item.author_name}
          </div>
        )}

        {/* Read more button */}
        <div className="flex items-center justify-between">
          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary text-sm"
            onClick={(e) => e.stopPropagation()}
          >
            Read Article
            <svg className="ml-1.5 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>

          {/* Optional: Share button or bookmark */}
          <button
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
            onClick={(e) => {
              e.stopPropagation()
              // Add share functionality here
              if (navigator.share) {
                navigator.share({
                  title: item.title,
                  url: item.url
                })
              }
            }}
            title="Share article"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
            </svg>
          </button>
        </div>
      </div>
    </article>
  )
}