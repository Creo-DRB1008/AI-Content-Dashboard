const sql = require('mssql');
const logger = require('../utils/logger');

// Database configuration
const dbConfig = {
  server: process.env.DB_SERVER,
  database: process.env.DB_DATABASE,
  user: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD,
  options: {
    encrypt: true,
    trustServerCertificate: true, // For self-signed certificates
    enableArithAbort: true,
    connectTimeout: 30000,
    requestTimeout: 30000,
  },
  pool: {
    max: 10,
    min: 0,
    idleTimeoutMillis: 30000,
  },
};

let pool = null;

/**
 * Initialize database connection
 */
async function initializeDatabase() {
  try {
    // Validate required environment variables
    const required = ['DB_SERVER', 'DB_DATABASE', 'DB_USERNAME', 'DB_PASSWORD'];
    const missing = required.filter(key => !process.env[key]);
    
    if (missing.length > 0) {
      throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
    }

    logger.info('Initializing database connection...');
    pool = new sql.ConnectionPool(dbConfig);
    await pool.connect();
    
    // Test the connection
    const result = await pool.request().query('SELECT @@VERSION as version');
    logger.info('Database connected successfully');
    logger.info(`SQL Server version: ${result.recordset[0].version.split('\n')[0]}`);
    
    return pool;
  } catch (error) {
    logger.error('Database connection failed:', error);
    throw error;
  }
}

/**
 * Get database connection pool
 */
function getPool() {
  if (!pool) {
    throw new Error('Database not initialized. Call initializeDatabase() first.');
  }
  return pool;
}

/**
 * Close database connection
 */
async function closeDatabase() {
  if (pool) {
    try {
      await pool.close();
      pool = null;
      logger.info('Database connection closed');
    } catch (error) {
      logger.error('Error closing database connection:', error);
    }
  }
}

/**
 * Execute a query with error handling
 */
async function executeQuery(query, params = {}) {
  try {
    const connectionPool = getPool();
    const request = connectionPool.request();
    
    // Add parameters to the request
    Object.entries(params).forEach(([key, { type, value }]) => {
      request.input(key, type, value);
    });
    
    const result = await request.query(query);
    return result;
  } catch (error) {
    logger.error('Query execution failed:', { query, error: error.message });
    throw error;
  }
}

/**
 * Check if database connection is healthy
 */
async function checkHealth() {
  try {
    const result = await executeQuery('SELECT 1 as health_check');
    return result.recordset[0].health_check === 1;
  } catch (error) {
    logger.error('Database health check failed:', error);
    return false;
  }
}

module.exports = {
  initializeDatabase,
  getPool,
  closeDatabase,
  executeQuery,
  checkHealth,
  sql
};
