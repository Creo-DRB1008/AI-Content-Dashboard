const express = require('express');
const { checkHealth } = require('../config/database');
const logger = require('../utils/logger');

const router = express.Router();

/**
 * Health check endpoint
 * GET /api/health
 */
router.get('/', async (req, res) => {
  try {
    const dbHealthy = await checkHealth();
    const status = dbHealthy ? 'healthy' : 'unhealthy';
    const statusCode = dbHealthy ? 200 : 503;

    const healthData = {
      status,
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      database: dbHealthy ? 'connected' : 'disconnected',
      memory: process.memoryUsage(),
      version: process.env.npm_package_version || '1.0.0'
    };

    logger.info('Health check performed', { status, database: healthData.database });
    res.status(statusCode).json(healthData);
  } catch (error) {
    logger.error('Health check failed:', error);
    res.status(503).json({
      status: 'error',
      timestamp: new Date().toISOString(),
      error: 'Health check failed',
      message: error.message
    });
  }
});

/**
 * Detailed health check endpoint
 * GET /api/health/detailed
 */
router.get('/detailed', async (req, res) => {
  try {
    const dbHealthy = await checkHealth();
    
    const healthData = {
      status: dbHealthy ? 'healthy' : 'unhealthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      environment: process.env.NODE_ENV || 'development',
      database: {
        status: dbHealthy ? 'connected' : 'disconnected',
        server: process.env.DB_SERVER ? 'configured' : 'not configured',
        database: process.env.DB_DATABASE ? 'configured' : 'not configured'
      },
      system: {
        memory: process.memoryUsage(),
        platform: process.platform,
        nodeVersion: process.version,
        pid: process.pid
      },
      version: process.env.npm_package_version || '1.0.0'
    };

    const statusCode = dbHealthy ? 200 : 503;
    res.status(statusCode).json(healthData);
  } catch (error) {
    logger.error('Detailed health check failed:', error);
    res.status(503).json({
      status: 'error',
      timestamp: new Date().toISOString(),
      error: 'Detailed health check failed',
      message: error.message
    });
  }
});

module.exports = router;
