import sql from 'mssql'

// Check if required environment variables are set
function validateEnvironment() {
  const required = ['DB_SERVER', 'DB_DATABASE', 'DB_USERNAME', 'DB_PASSWORD']
  const missing = required.filter(key => !process.env[key])

  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(', ')}. Please set these in your .env.local file or Vercel environment variables.`)
  }
}

// Database configuration
function getDbConfig() {
  validateEnvironment()

  return {
    server: process.env.DB_SERVER,
    database: process.env.DB_DATABASE,
    user: process.env.DB_USERNAME,
    password: process.env.DB_PASSWORD,
    options: {
      encrypt: true, // Use encryption for Azure SQL
      trustServerCertificate: true, // Trust self-signed certificates
      enableArithAbort: true,
    },
    pool: {
      max: 10,
      min: 0,
      idleTimeoutMillis: 30000,
    },
  }
}

// Connection pool instance
let pool = null

/**
 * Get a database connection pool
 * @returns {Promise<sql.ConnectionPool>}
 */
export async function getPool() {
  if (!pool) {
    const dbConfig = getDbConfig()
    pool = new sql.ConnectionPool(dbConfig)
    await pool.connect()
  }
  return pool
}

/**
 * Close the database connection pool
 */
export async function closePool() {
  if (pool) {
    await pool.close()
    pool = null
  }
}

/**
 * Execute a query with automatic connection management
 * @param {string} query - SQL query string
 * @param {Object} params - Query parameters
 * @returns {Promise<sql.IResult>}
 */
export async function executeQuery(query, params = {}) {
  const connectionPool = await getPool()
  const request = connectionPool.request()

  // Add parameters to the request
  Object.entries(params).forEach(([key, { type, value }]) => {
    request.input(key, type, value)
  })

  return await request.query(query)
}

export { sql }
export default { getPool, closePool, executeQuery, sql }
