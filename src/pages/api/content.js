import { exec } from 'child_process'
import { promisify } from 'util'

const execPromise = promisify(exec)

// Mock data as fallback if database connection fails
const mockContent = [
  {
    id: '1',
    title: 'The Future of AI in Healthcare',
    content: 'AI is revolutionizing healthcare with predictive analytics and personalized medicine...',
    url: 'https://example.com/ai-healthcare',
    source: 'twitter',
    published_at: new Date().toISOString(),
    likes: 120,
    shares: 45,
    comments: 23
  },
  {
    id: '2',
    title: 'Machine Learning Trends in 2025',
    content: 'The top machine learning trends to watch for in 2025 include...',
    url: 'https://example.com/ml-trends',
    source: 'linkedin',
    published_at: new Date().toISOString(),
    likes: 89,
    shares: 34,
    comments: 12
  },
  {
    id: '3',
    title: 'New Research in Natural Language Processing',
    content: 'Researchers have made significant breakthroughs in NLP...',
    url: 'https://example.com/nlp-research',
    source: 'rss',
    published_at: new Date().toISOString(),
    likes: 56,
    shares: 23,
    comments: 8
  },
  {
    id: '4',
    title: 'Ethics in Artificial Intelligence',
    content: 'The ethical considerations of AI development are becoming increasingly important...',
    url: 'https://example.com/ai-ethics',
    source: 'twitter',
    published_at: new Date().toISOString(),
    likes: 210,
    shares: 78,
    comments: 45
  },
  {
    id: '5',
    title: 'How Companies are Implementing AI',
    content: 'Leading companies are implementing AI in these innovative ways...',
    url: 'https://example.com/ai-implementation',
    source: 'linkedin',
    published_at: new Date().toISOString(),
    likes: 145,
    shares: 67,
    comments: 32
  },
  {
    id: '6',
    title: 'The Role of Deep Learning in Computer Vision',
    content: 'Deep learning has transformed computer vision applications...',
    url: 'https://example.com/deep-learning-vision',
    source: 'rss',
    published_at: new Date().toISOString(),
    likes: 78,
    shares: 34,
    comments: 15
  }
];

export default async function handler(req, res) {
  try {
    // Get query parameters
    const { date, source, limit } = req.query

    // Build command with optional parameters
    let command = 'python src/api/get_content.py'
    if (date) command += ` --date ${date}`
    if (source) command += ` --source ${source}`
    if (limit) command += ` --limit ${limit}`

    // Try to execute Python script to fetch content from database
    const { stdout } = await execPromise(command)
    const content = JSON.parse(stdout)

    // Return real data from database
    res.status(200).json(content)
  } catch (error) {
    console.error('Error fetching content from database:', error)
    console.log('Falling back to mock data')

    // Fall back to mock data if database connection fails
    res.status(200).json(mockContent)
  }
}