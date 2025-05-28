#!/usr/bin/env node

/**
 * Data collection script for GitHub Actions
 * This script calls the Render backend API to trigger data collection
 */

const axios = require('axios');
require('dotenv').config();

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:3000';
const API_KEY = process.env.API_KEY;

async function collectData() {
  try {
    console.log('🚀 Starting data collection...');
    console.log(`Backend URL: ${BACKEND_URL}`);
    
    if (!API_KEY) {
      throw new Error('API_KEY environment variable is required');
    }

    const startTime = Date.now();
    
    // Make request to backend API
    const response = await axios.post(
      `${BACKEND_URL}/api/data/collect`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 300000 // 5 minute timeout
      }
    );

    const duration = Date.now() - startTime;
    const result = response.data;

    console.log('✅ Data collection completed successfully!');
    console.log(`📊 Results:`);
    console.log(`   - Duration: ${duration}ms`);
    console.log(`   - Items collected: ${result.collected || 0}`);
    console.log(`   - Items summarized: ${result.summarized || 0}`);
    
    if (result.errors && result.errors.length > 0) {
      console.log(`⚠️  Errors encountered:`);
      result.errors.forEach(error => console.log(`   - ${error}`));
    }

    // Exit with success
    process.exit(0);

  } catch (error) {
    console.error('❌ Data collection failed:');
    
    if (error.response) {
      // API responded with error
      console.error(`   Status: ${error.response.status}`);
      console.error(`   Message: ${error.response.data?.message || error.response.statusText}`);
      if (error.response.data?.errors) {
        console.error(`   Errors:`, error.response.data.errors);
      }
    } else if (error.request) {
      // Request timeout or network error
      console.error(`   Network error: ${error.message}`);
      console.error(`   Check if backend service is running at: ${BACKEND_URL}`);
    } else {
      // Other error
      console.error(`   Error: ${error.message}`);
    }

    // Exit with error
    process.exit(1);
  }
}

// Handle process signals
process.on('SIGINT', () => {
  console.log('\n🛑 Data collection interrupted');
  process.exit(1);
});

process.on('SIGTERM', () => {
  console.log('\n🛑 Data collection terminated');
  process.exit(1);
});

// Run the collection
if (require.main === module) {
  collectData();
}

module.exports = { collectData };
