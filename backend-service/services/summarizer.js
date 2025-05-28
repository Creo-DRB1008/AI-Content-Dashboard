const axios = require('axios');
const logger = require('../utils/logger');

/**
 * Summarize content using AI API (OpenAI or compatible)
 */
async function summarizeContent(content, title = '') {
  try {
    // Check if summarization is enabled
    if (process.env.SUMMARIZATION_ENABLED !== 'true') {
      logger.debug('Summarization disabled, skipping');
      return null;
    }

    // Check if required environment variables are set
    if (!process.env.SUMMARIZATION_API_KEY || !process.env.SUMMARIZATION_API_URL) {
      logger.warn('Summarization API not configured, skipping');
      return null;
    }

    // Skip if content is too short
    if (!content || content.length < 100) {
      logger.debug('Content too short for summarization');
      return null;
    }

    // Prepare the prompt
    const prompt = createSummarizationPrompt(content, title);
    
    // Make API request
    const response = await axios.post(
      process.env.SUMMARIZATION_API_URL,
      {
        model: process.env.SUMMARIZATION_MODEL || 'gpt-3.5-turbo',
        messages: [
          {
            role: 'system',
            content: 'You are a helpful assistant that creates concise, informative summaries of AI-related articles. Focus on key insights, developments, and implications.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        max_tokens: parseInt(process.env.SUMMARIZATION_MAX_TOKENS) || 150,
        temperature: 0.3,
        top_p: 1,
        frequency_penalty: 0,
        presence_penalty: 0
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.SUMMARIZATION_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 30000 // 30 second timeout
      }
    );

    if (response.data?.choices?.[0]?.message?.content) {
      const summary = response.data.choices[0].message.content.trim();
      logger.debug('Successfully generated summary', { 
        originalLength: content.length, 
        summaryLength: summary.length 
      });
      return summary;
    } else {
      logger.warn('Unexpected API response format', { response: response.data });
      return null;
    }

  } catch (error) {
    if (error.response) {
      // API responded with error status
      logger.error('Summarization API error:', {
        status: error.response.status,
        statusText: error.response.statusText,
        data: error.response.data
      });
    } else if (error.request) {
      // Request was made but no response received
      logger.error('Summarization API timeout or network error:', error.message);
    } else {
      // Something else happened
      logger.error('Summarization error:', error.message);
    }
    return null;
  }
}

/**
 * Create a summarization prompt
 */
function createSummarizationPrompt(content, title) {
  const cleanContent = content.substring(0, 3000); // Limit content length
  
  return `Please provide a concise summary of this AI-related article in 2-3 sentences. Focus on the key developments, implications, and main points.

Title: ${title}

Content: ${cleanContent}

Summary:`;
}

/**
 * Batch summarize multiple content items
 */
async function batchSummarize(items, batchSize = 5) {
  const results = [];
  
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    
    logger.info(`Processing summarization batch ${Math.floor(i / batchSize) + 1}/${Math.ceil(items.length / batchSize)}`);
    
    const batchPromises = batch.map(async (item) => {
      try {
        const summary = await summarizeContent(item.content, item.title);
        return { ...item, summary };
      } catch (error) {
        logger.error(`Error summarizing item ${item.id}:`, error);
        return { ...item, summary: null };
      }
    });
    
    const batchResults = await Promise.all(batchPromises);
    results.push(...batchResults);
    
    // Add delay between batches to respect rate limits
    if (i + batchSize < items.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  return results;
}

/**
 * Test summarization configuration
 */
async function testSummarization() {
  const testContent = `
    Artificial Intelligence continues to advance rapidly with new developments in large language models. 
    Recent breakthroughs in transformer architectures have enabled more sophisticated reasoning capabilities. 
    Companies are investing heavily in AI research and development, leading to improved performance across 
    various tasks including natural language processing, computer vision, and robotics.
  `;
  
  try {
    const summary = await summarizeContent(testContent, 'AI Development Test');
    if (summary) {
      logger.info('Summarization test successful', { summary });
      return { success: true, summary };
    } else {
      logger.warn('Summarization test returned null');
      return { success: false, error: 'No summary generated' };
    }
  } catch (error) {
    logger.error('Summarization test failed:', error);
    return { success: false, error: error.message };
  }
}

module.exports = {
  summarizeContent,
  batchSummarize,
  testSummarization,
  createSummarizationPrompt
};
