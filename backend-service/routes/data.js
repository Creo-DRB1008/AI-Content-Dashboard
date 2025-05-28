const express = require('express');
const { executeQuery, sql } = require('../config/database');
const logger = require('../utils/logger');
const { collectRSSData } = require('../services/rssCollector');
const { summarizeContent } = require('../services/summarizer');

const router = express.Router();

/**
 * Trigger data collection (for GitHub Actions)
 * POST /api/data/collect
 * Headers: Authorization: Bearer <API_KEY>
 */
router.post('/collect', async (req, res) => {
  try {
    // Verify API key for security
    const apiKey = req.headers.authorization?.replace('Bearer ', '');
    if (!apiKey || apiKey !== process.env.API_KEY) {
      logger.warn('Unauthorized data collection attempt', { ip: req.ip });
      return res.status(401).json({
        error: 'Unauthorized',
        message: 'Valid API key required'
      });
    }

    logger.info('Starting data collection process');
    
    const startTime = Date.now();
    let totalCollected = 0;
    let totalSummarized = 0;
    let errors = [];

    try {
      // Collect RSS data
      logger.info('Collecting RSS data...');
      const rssResults = await collectRSSData();
      
      for (const result of rssResults) {
        if (result.success) {
          totalCollected += result.items.length;
          
          // Process each item
          for (const item of result.items) {
            try {
              // Generate summary if enabled and content exists
              let summary = null;
              if (process.env.SUMMARIZATION_ENABLED === 'true' && item.content) {
                summary = await summarizeContent(item.content, item.title);
                if (summary) totalSummarized++;
              }

              // Save to database
              await saveContentItem({
                ...item,
                summary,
                source: 'rss'
              });
            } catch (itemError) {
              logger.error('Error processing item:', itemError);
              errors.push(`Item processing error: ${itemError.message}`);
            }
          }
        } else {
          errors.push(`RSS collection error: ${result.error}`);
        }
      }

      const duration = Date.now() - startTime;
      
      const result = {
        success: true,
        duration: `${duration}ms`,
        collected: totalCollected,
        summarized: totalSummarized,
        errors: errors.length > 0 ? errors : undefined,
        timestamp: new Date().toISOString()
      };

      logger.info('Data collection completed', result);
      res.json(result);

    } catch (collectionError) {
      logger.error('Data collection failed:', collectionError);
      res.status(500).json({
        success: false,
        error: 'Data collection failed',
        message: collectionError.message,
        duration: `${Date.now() - startTime}ms`,
        timestamp: new Date().toISOString()
      });
    }

  } catch (error) {
    logger.error('Data collection endpoint error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
});

/**
 * Get collection status/history
 * GET /api/data/status
 */
router.get('/status', async (req, res) => {
  try {
    const queries = {
      lastCollection: `
        SELECT TOP 1 collected_at 
        FROM content 
        ORDER BY collected_at DESC
      `,
      todayCount: `
        SELECT COUNT(*) as count 
        FROM content 
        WHERE CAST(collected_at AS DATE) = CAST(GETDATE() AS DATE)
      `,
      recentSources: `
        SELECT source, COUNT(*) as count, MAX(collected_at) as last_collected
        FROM content 
        WHERE collected_at >= DATEADD(day, -1, GETDATE())
        GROUP BY source
      `
    };

    const [lastResult, todayResult, sourcesResult] = await Promise.all([
      executeQuery(queries.lastCollection),
      executeQuery(queries.todayCount),
      executeQuery(queries.recentSources)
    ]);

    const status = {
      lastCollection: lastResult.recordset[0]?.collected_at || null,
      todayCount: todayResult.recordset[0].count,
      recentSources: sourcesResult.recordset.map(row => ({
        source: row.source,
        count: row.count,
        lastCollected: row.last_collected
      })),
      timestamp: new Date().toISOString()
    };

    res.json(status);
  } catch (error) {
    logger.error('Error fetching collection status:', error);
    res.status(500).json({
      error: 'Failed to fetch collection status',
      message: error.message
    });
  }
});

/**
 * Save content item to database
 */
async function saveContentItem(item) {
  const query = `
    INSERT INTO content (
      id, title, content, summary, url, source, source_id,
      published_at, collected_at, author_name, author_url,
      likes, shares, comments, sentiment_score
    ) VALUES (
      @id, @title, @content, @summary, @url, @source, @source_id,
      @published_at, @collected_at, @author_name, @author_url,
      @likes, @shares, @comments, @sentiment_score
    )
  `;

  const params = {
    id: { type: sql.UniqueIdentifier, value: item.id },
    title: { type: sql.NVarChar, value: item.title },
    content: { type: sql.NText, value: item.content },
    summary: { type: sql.NText, value: item.summary },
    url: { type: sql.NVarChar, value: item.url },
    source: { type: sql.NVarChar, value: item.source },
    source_id: { type: sql.NVarChar, value: item.source_id },
    published_at: { type: sql.DateTime, value: item.published_at },
    collected_at: { type: sql.DateTime, value: new Date() },
    author_name: { type: sql.NVarChar, value: item.author_name },
    author_url: { type: sql.NVarChar, value: item.author_url },
    likes: { type: sql.Int, value: item.likes },
    shares: { type: sql.Int, value: item.shares },
    comments: { type: sql.Int, value: item.comments },
    sentiment_score: { type: sql.Float, value: item.sentiment_score }
  };

  await executeQuery(query, params);
}

module.exports = router;
