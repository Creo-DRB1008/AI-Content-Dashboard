const express = require('express');
const { executeQuery, sql } = require('../config/database');
const logger = require('../utils/logger');

const router = express.Router();

/**
 * Get content with optional filters
 * GET /api/content?date=YYYY-MM-DD&source=rss&limit=30
 */
router.get('/', async (req, res) => {
  try {
    const { date, source, limit = 30 } = req.query;

    // Build SQL query with optional filters
    let query = `
      SELECT TOP (@limit)
        id,
        title,
        content,
        summary,
        url,
        source,
        published_at,
        collected_at,
        author_name,
        author_url,
        likes,
        shares,
        comments,
        sentiment_score
      FROM content
      WHERE 1=1
    `;

    const params = {
      limit: { type: sql.Int, value: parseInt(limit) }
    };

    // Add date filter if provided
    if (date) {
      query += ` AND CAST(published_at AS DATE) = @date`;
      params.date = { type: sql.Date, value: new Date(date) };
    }

    // Add source filter if provided
    if (source) {
      query += ` AND source = @source`;
      params.source = { type: sql.VarChar, value: source };
    }

    // Order by published date (most recent first)
    query += ` ORDER BY published_at DESC`;

    // Execute query
    const result = await executeQuery(query, params);

    // Format the results
    const content = result.recordset.map(row => ({
      id: row.id,
      title: row.title,
      content: row.content,
      summary: row.summary,
      url: row.url,
      source: row.source,
      published_at: row.published_at,
      collected_at: row.collected_at,
      author_name: row.author_name,
      author_url: row.author_url,
      likes: row.likes,
      shares: row.shares,
      comments: row.comments,
      sentiment_score: row.sentiment_score
    }));

    logger.info(`Retrieved ${content.length} content items`, {
      filters: { date, source, limit },
      count: content.length
    });

    res.json(content);
  } catch (error) {
    logger.error('Error fetching content:', error);
    res.status(500).json({
      error: 'Failed to fetch content',
      message: error.message
    });
  }
});

/**
 * Get available dates with content count
 * GET /api/content/dates
 */
router.get('/dates', async (req, res) => {
  try {
    const query = `
      SELECT
        CAST(published_at AS DATE) as date,
        COUNT(*) as count
      FROM content
      WHERE published_at IS NOT NULL
      GROUP BY CAST(published_at AS DATE)
      ORDER BY date DESC
    `;

    const result = await executeQuery(query);

    // Format the results
    const dates = result.recordset.map(row => ({
      date: row.date.toISOString().split('T')[0], // Format as YYYY-MM-DD
      count: row.count
    }));

    logger.info(`Retrieved ${dates.length} available dates`);
    res.json(dates);
  } catch (error) {
    logger.error('Error fetching dates:', error);
    res.status(500).json({
      error: 'Failed to fetch dates',
      message: error.message
    });
  }
});

/**
 * Get content statistics
 * GET /api/content/stats
 */
router.get('/stats', async (req, res) => {
  try {
    const queries = {
      total: 'SELECT COUNT(*) as count FROM content',
      bySource: `
        SELECT source, COUNT(*) as count
        FROM content
        GROUP BY source
        ORDER BY count DESC
      `,
      recent: `
        SELECT COUNT(*) as count
        FROM content
        WHERE published_at >= DATEADD(day, -7, GETDATE())
      `,
      withSummary: `
        SELECT COUNT(*) as count
        FROM content
        WHERE summary IS NOT NULL AND summary != ''
      `
    };

    const [totalResult, bySourceResult, recentResult, withSummaryResult] = await Promise.all([
      executeQuery(queries.total),
      executeQuery(queries.bySource),
      executeQuery(queries.recent),
      executeQuery(queries.withSummary)
    ]);

    const stats = {
      total: totalResult.recordset[0].count,
      recent: recentResult.recordset[0].count,
      withSummary: withSummaryResult.recordset[0].count,
      bySource: bySourceResult.recordset.map(row => ({
        source: row.source,
        count: row.count
      }))
    };

    logger.info('Retrieved content statistics', stats);
    res.json(stats);
  } catch (error) {
    logger.error('Error fetching content statistics:', error);
    res.status(500).json({
      error: 'Failed to fetch content statistics',
      message: error.message
    });
  }
});

module.exports = router;
