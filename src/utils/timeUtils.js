/**
 * Utility functions for time formatting and display
 */
import { formatDistanceToNow, format, isToday, isYesterday, parseISO } from 'date-fns'

/**
 * Format a date for display with smart relative/absolute formatting
 * @param {string|Date} dateInput - The date to format
 * @returns {string} Formatted date string
 */
export function formatSmartDate(dateInput) {
  try {
    const date = typeof dateInput === 'string' ? parseISO(dateInput) : dateInput
    
    if (!date || isNaN(date.getTime())) {
      return 'Unknown date'
    }

    const now = new Date()
    const diffInHours = Math.abs(now - date) / (1000 * 60 * 60)

    // If less than 1 hour ago, show minutes
    if (diffInHours < 1) {
      const diffInMinutes = Math.floor(Math.abs(now - date) / (1000 * 60))
      if (diffInMinutes < 1) {
        return 'Just now'
      }
      return `${diffInMinutes}m ago`
    }

    // If less than 24 hours ago, show hours
    if (diffInHours < 24) {
      const hours = Math.floor(diffInHours)
      return `${hours}h ago`
    }

    // If today, show time
    if (isToday(date)) {
      return format(date, 'h:mm a')
    }

    // If yesterday, show "Yesterday"
    if (isYesterday(date)) {
      return 'Yesterday'
    }

    // If within the last week, show day name
    if (diffInHours < 24 * 7) {
      return format(date, 'EEEE')
    }

    // If within the current year, show month and day
    if (date.getFullYear() === now.getFullYear()) {
      return format(date, 'MMM d')
    }

    // Otherwise, show full date
    return format(date, 'MMM d, yyyy')
  } catch (error) {
    console.error('Error formatting date:', error)
    return 'Invalid date'
  }
}

/**
 * Get a detailed timestamp for tooltips
 * @param {string|Date} dateInput - The date to format
 * @returns {string} Full timestamp string
 */
export function formatFullTimestamp(dateInput) {
  try {
    const date = typeof dateInput === 'string' ? parseISO(dateInput) : dateInput
    
    if (!date || isNaN(date.getTime())) {
      return 'Unknown date'
    }

    return format(date, 'EEEE, MMMM d, yyyy \'at\' h:mm a')
  } catch (error) {
    console.error('Error formatting full timestamp:', error)
    return 'Invalid date'
  }
}

/**
 * Get relative time with better precision
 * @param {string|Date} dateInput - The date to format
 * @returns {string} Relative time string
 */
export function formatRelativeTime(dateInput) {
  try {
    const date = typeof dateInput === 'string' ? parseISO(dateInput) : dateInput
    
    if (!date || isNaN(date.getTime())) {
      return 'Unknown time'
    }

    return formatDistanceToNow(date, { 
      addSuffix: true,
      includeSeconds: true
    })
  } catch (error) {
    console.error('Error formatting relative time:', error)
    return 'Invalid time'
  }
}
