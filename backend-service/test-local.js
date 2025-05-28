#!/usr/bin/env node

/**
 * Local testing script for the backend service
 * Run this to test the backend before deploying to Render
 */

const axios = require('axios');
require('dotenv').config();

const BASE_URL = 'http://localhost:3000';

async function testEndpoint(method, endpoint, data = null, headers = {}) {
  try {
    console.log(`\n🔍 Testing ${method} ${endpoint}`);
    
    const config = {
      method,
      url: `${BASE_URL}${endpoint}`,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      timeout: 10000
    };
    
    if (data) {
      config.data = data;
    }
    
    const response = await axios(config);
    console.log(`✅ Status: ${response.status}`);
    console.log(`📄 Response:`, JSON.stringify(response.data, null, 2));
    return response.data;
  } catch (error) {
    if (error.response) {
      console.log(`❌ Status: ${error.response.status}`);
      console.log(`📄 Error:`, JSON.stringify(error.response.data, null, 2));
    } else {
      console.log(`❌ Error: ${error.message}`);
    }
    return null;
  }
}

async function runTests() {
  console.log('🚀 Starting backend service tests...');
  console.log(`Base URL: ${BASE_URL}`);
  
  // Test 1: Root endpoint
  await testEndpoint('GET', '/');
  
  // Test 2: Health check
  await testEndpoint('GET', '/api/health');
  
  // Test 3: Detailed health check
  await testEndpoint('GET', '/api/health/detailed');
  
  // Test 4: Get content
  await testEndpoint('GET', '/api/content?limit=5');
  
  // Test 5: Get dates
  await testEndpoint('GET', '/api/content/dates');
  
  // Test 6: Get stats
  await testEndpoint('GET', '/api/content/stats');
  
  // Test 7: Get collection status
  await testEndpoint('GET', '/api/data/status');
  
  // Test 8: Test data collection (if API key is set)
  if (process.env.API_KEY) {
    console.log('\n⚠️  Testing data collection (this will actually collect data!)');
    console.log('Press Ctrl+C to cancel, or wait 5 seconds to continue...');
    
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    await testEndpoint('POST', '/api/data/collect', {}, {
      'Authorization': `Bearer ${process.env.API_KEY}`
    });
  } else {
    console.log('\n⚠️  Skipping data collection test (API_KEY not set)');
  }
  
  console.log('\n🎉 Tests completed!');
}

// Handle Ctrl+C
process.on('SIGINT', () => {
  console.log('\n🛑 Tests interrupted');
  process.exit(0);
});

if (require.main === module) {
  runTests().catch(error => {
    console.error('❌ Test runner failed:', error);
    process.exit(1);
  });
}

module.exports = { testEndpoint, runTests };
