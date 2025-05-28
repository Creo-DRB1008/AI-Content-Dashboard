#!/usr/bin/env python3
"""
Test script for the summarization service.
"""
import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.summarization_service import summarization_service
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('test_summarization')

def test_summarization_service():
    """Test the summarization service with sample content."""
    print("\n=== Testing Summarization Service ===")
    
    # Sample article content
    sample_title = "OpenAI Releases GPT-4 Turbo with Enhanced Capabilities"
    sample_content = """
    OpenAI has announced the release of GPT-4 Turbo, a more powerful and efficient version of their flagship language model. 
    The new model features improved reasoning capabilities, better understanding of context, and enhanced performance across 
    various tasks including coding, mathematics, and creative writing. GPT-4 Turbo also includes a larger context window 
    that can process up to 128,000 tokens, allowing for more comprehensive analysis of longer documents. The model has been 
    trained on data up to April 2024 and includes significant improvements in factual accuracy and reduced hallucinations. 
    OpenAI claims that GPT-4 Turbo is 3x faster than its predecessor while maintaining the same level of quality. The model 
    is now available through the OpenAI API with competitive pricing that makes it more accessible for developers and 
    businesses looking to integrate advanced AI capabilities into their applications.
    """
    
    try:
        print(f"Testing summarization for: {sample_title}")
        print(f"Content length: {len(sample_content)} characters")
        
        # Test if summarization is enabled
        if not summarization_service.enabled:
            print("❌ Summarization is disabled. Check your API key configuration.")
            return False
        
        # Generate summary
        summary = summarization_service.generate_summary(sample_content, sample_title)
        
        if summary:
            print("✅ Summary generated successfully!")
            print(f"Summary: {summary}")
            print(f"Summary length: {len(summary)} characters")
            return True
        else:
            print("❌ Failed to generate summary")
            return False
            
    except Exception as e:
        print(f"❌ Error testing summarization: {str(e)}")
        return False

def test_content_cleaning():
    """Test the content cleaning functionality."""
    print("\n=== Testing Content Cleaning ===")
    
    # Sample content with HTML tags and entities
    dirty_content = """
    <p>This is a <strong>test article</strong> with HTML tags.</p>
    <div>It contains &amp; HTML entities &lt;like this&gt;.</div>
    <img src="test.jpg" alt="Test image" />
    <a href="https://example.com">Link to example</a>
    
    Multiple    spaces    and
    
    line breaks should be cleaned up.
    """
    
    try:
        cleaned = summarization_service.clean_content(dirty_content)
        print("Original content:")
        print(repr(dirty_content))
        print("\nCleaned content:")
        print(repr(cleaned))
        
        # Check if HTML tags are removed
        if '<' not in cleaned and '>' not in cleaned:
            print("✅ HTML tags removed successfully")
        else:
            print("❌ HTML tags not properly removed")
            return False
        
        # Check if HTML entities are decoded
        if '&amp;' not in cleaned and '&lt;' not in cleaned:
            print("✅ HTML entities decoded successfully")
        else:
            print("❌ HTML entities not properly decoded")
            return False
        
        # Check if extra whitespace is cleaned
        if '    ' not in cleaned and '\n\n' not in cleaned:
            print("✅ Extra whitespace cleaned successfully")
        else:
            print("❌ Extra whitespace not properly cleaned")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing content cleaning: {str(e)}")
        return False

def test_batch_summarization():
    """Test batch summarization functionality."""
    print("\n=== Testing Batch Summarization ===")
    
    # Sample articles
    articles = [
        {
            'id': 'article_1',
            'title': 'AI Breakthrough in Medical Diagnosis',
            'content': 'Researchers have developed a new AI system that can diagnose diseases with 95% accuracy...'
        },
        {
            'id': 'article_2', 
            'title': 'Machine Learning in Finance',
            'content': 'Financial institutions are increasingly adopting machine learning algorithms for fraud detection...'
        }
    ]
    
    try:
        if not summarization_service.enabled:
            print("⚠️ Summarization is disabled. Skipping batch test.")
            return True
        
        summaries = summarization_service.generate_summaries_batch(articles)
        
        print(f"Generated {len(summaries)} summaries out of {len(articles)} articles")
        
        for article_id, summary in summaries.items():
            print(f"Article {article_id}: {summary[:100]}...")
        
        if len(summaries) > 0:
            print("✅ Batch summarization working")
            return True
        else:
            print("❌ No summaries generated in batch")
            return False
            
    except Exception as e:
        print(f"❌ Error testing batch summarization: {str(e)}")
        return False

def main():
    """Run all summarization tests."""
    print("Summarization Service Test Suite")
    print("=" * 40)
    
    tests = [
        ("Content Cleaning", test_content_cleaning),
        ("Summarization Service", test_summarization_service),
        ("Batch Summarization", test_batch_summarization)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\nRunning test: {test_name}")
        result = test_func()
        results[test_name] = "PASS" if result else "FAIL"
    
    # Print summary
    print("\n" + "=" * 40)
    print("Test Results Summary")
    print("=" * 40)
    for test_name, result in results.items():
        status_icon = "✅" if result == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {result}")
    
    # Overall result
    all_passed = all(result == "PASS" for result in results.values())
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️ Some tests failed. Check your configuration.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
