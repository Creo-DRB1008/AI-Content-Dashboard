const Parser = require('rss-parser');
const { v4: uuidv4 } = require('uuid');
const logger = require('../utils/logger');

const parser = new Parser({
  timeout: 10000,
  headers: {
    'User-Agent': 'AI-Dashboard-Bot/1.0'
  }
});

// RSS Feed URLs (same as in the original config)
const RSS_FEEDS = {
  'wired_ai': 'https://www.wired.com/feed/tag/artificial-intelligence/latest/rss',
  'mit_ai': 'https://news.mit.edu/topic/artificial-intelligence2-rss.xml',
  'google_ai': 'https://ai.googleblog.com/feeds/posts/default',
  'nvidia_ai': 'https://blogs.nvidia.com/blog/category/ai/feed/',
  'venturebeat_ai': 'https://venturebeat.com/category/ai/feed/',
  'techcrunch_ai': 'https://techcrunch.com/tag/artificial-intelligence/feed/',
  'microsoft_ai': 'https://techcommunity.microsoft.com/gxcuf89792/rss/board?board.id=AI_Blog',
  'ibm_ai': 'https://research.ibm.com/blog/rss',
  'technologyreview_ai': 'https://www.technologyreview.com/feed/topic/artificial-intelligence/',
  'deepmind_ai': 'https://www.deepmind.com/blog/rss.xml',
  'openai_blog': 'https://openai.com/blog/rss',
  'theaireport': 'https://theaireport.substack.com/feed',
  'jack_clark': 'https://jack-clark.net/index.xml',
  'bair_berkeley': 'https://bair.berkeley.edu/blog/feed.xml',
  'thegradient': 'https://thegradient.pub/rss/'
};

/**
 * Collect data from all RSS feeds
 */
async function collectRSSData() {
  const results = [];
  
  for (const [feedName, feedUrl] of Object.entries(RSS_FEEDS)) {
    try {
      logger.info(`Collecting from ${feedName}: ${feedUrl}`);
      
      const feed = await parser.parseURL(feedUrl);
      const items = [];
      
      // Process recent items (last 7 days)
      const sevenDaysAgo = new Date();
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
      
      for (const item of feed.items) {
        try {
          const publishedDate = new Date(item.pubDate || item.isoDate);
          
          // Skip items older than 7 days
          if (publishedDate < sevenDaysAgo) {
            continue;
          }
          
          const processedItem = {
            id: uuidv4(),
            title: cleanText(item.title),
            content: cleanText(item.content || item.summary || item.description),
            url: item.link,
            source_id: item.guid || item.link,
            published_at: publishedDate,
            author_name: extractAuthor(item),
            author_url: null,
            likes: null,
            shares: null,
            comments: null,
            sentiment_score: null
          };
          
          // Skip if essential fields are missing
          if (!processedItem.title || !processedItem.url) {
            logger.warn(`Skipping item with missing essential fields from ${feedName}`);
            continue;
          }
          
          items.push(processedItem);
        } catch (itemError) {
          logger.error(`Error processing item from ${feedName}:`, itemError);
        }
      }
      
      results.push({
        feedName,
        feedUrl,
        success: true,
        items,
        count: items.length
      });
      
      logger.info(`Collected ${items.length} items from ${feedName}`);
      
    } catch (error) {
      logger.error(`Error collecting from ${feedName}:`, error);
      results.push({
        feedName,
        feedUrl,
        success: false,
        error: error.message,
        items: [],
        count: 0
      });
    }
  }
  
  return results;
}

/**
 * Clean and normalize text content
 */
function cleanText(text) {
  if (!text) return null;
  
  return text
    .replace(/<[^>]*>/g, '') // Remove HTML tags
    .replace(/&nbsp;/g, ' ') // Replace &nbsp; with space
    .replace(/&amp;/g, '&') // Replace &amp; with &
    .replace(/&lt;/g, '<') // Replace &lt; with <
    .replace(/&gt;/g, '>') // Replace &gt; with >
    .replace(/&quot;/g, '"') // Replace &quot; with "
    .replace(/&#39;/g, "'") // Replace &#39; with '
    .replace(/\s+/g, ' ') // Replace multiple spaces with single space
    .trim();
}

/**
 * Extract author information from RSS item
 */
function extractAuthor(item) {
  if (item.creator) return item.creator;
  if (item.author) return item.author;
  if (item['dc:creator']) return item['dc:creator'];
  
  // Try to extract from content
  if (item.content) {
    const authorMatch = item.content.match(/by\s+([^<\n]+)/i);
    if (authorMatch) return authorMatch[1].trim();
  }
  
  return null;
}

/**
 * Check if content item already exists in database
 */
async function contentExists(sourceId, url) {
  try {
    const { executeQuery, sql } = require('../config/database');
    
    const query = `
      SELECT COUNT(*) as count 
      FROM content 
      WHERE source_id = @source_id OR url = @url
    `;
    
    const params = {
      source_id: { type: sql.NVarChar, value: sourceId },
      url: { type: sql.NVarChar, value: url }
    };
    
    const result = await executeQuery(query, params);
    return result.recordset[0].count > 0;
  } catch (error) {
    logger.error('Error checking content existence:', error);
    return false; // Assume it doesn't exist if we can't check
  }
}

module.exports = {
  collectRSSData,
  cleanText,
  extractAuthor,
  contentExists
};
