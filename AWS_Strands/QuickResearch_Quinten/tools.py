"""
Tools for Quick Research Quinten Agent

Provides atomic research tools following Strands framework patterns.
"""

import urllib.parse
import asyncio
import json
from typing import List, Dict, Any
import logging
from strands import tool
from crawl4ai import AsyncWebCrawler, BrowserConfig

# Configure logging for tools
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@tool
def generate_search_url(engine: str, keywords: List[str]) -> str:
    """
    Generate search URLs for conducting web research on specific topics.

    This tool creates search engine URLs with DuckDuckGo as the primary engine 
    due to better bot detection avoidance and cleaner results parsing.

    Args:
        engine: The search engine to use for URL generation (string)
               Supported: "duckduckgo", "bing", "google" 
               Recommended: "duckduckgo" (best for automated access)
        keywords: List of search terms to combine into a search query (list of strings)
                 Should be relevant keywords that describe what you're searching for
                 Example: ["Python", "tutorial"] or ["business", "contact", "email"]
                 Must contain at least one keyword

    Returns:
        A properly formatted, URL-encoded search URL optimized for web scraping
    """
    logger.info(f"generate_search_url called: engine='{engine}', keywords={keywords}")
    
    if not keywords:
        logger.error("Keywords list cannot be empty")
        raise ValueError("Keywords list cannot be empty")
    
    # Join keywords with spaces and URL encode
    query = " ".join(keywords)
    encoded_query = urllib.parse.quote_plus(query)
    
    engine = engine.lower()
    
    if engine == "duckduckgo":
        url = f"https://duckduckgo.com/?q={encoded_query}"
    elif engine == "bing":
        url = f"https://www.bing.com/search?q={encoded_query}"
    elif engine == "google":
        # Still available but not recommended due to bot detection
        logger.warning("Google search has known bot detection issues. Consider using 'duckduckgo' instead.")
        url = f"https://www.google.com/search?q={encoded_query}"
    else:
        logger.error(f"Unsupported engine '{engine}'. Supported: duckduckgo, bing, google")
        raise ValueError(f"Unsupported engine '{engine}'. Supported: duckduckgo, bing, google")
    
    logger.info(f"Generated search URL: {url}")
    return url


@tool
def process_web_content(url: str, timeout: int = 30) -> str:
    """
    Extract clean, readable content from web pages for AI analysis and research.

    Use this tool when you need to fetch web content and convert it into clean, structured format
    that's easy to analyze and extract information from. This is the primary tool for processing
    web pages during research workflows, converting raw HTML into readable markdown content.

    This tool handles the complete web content processing pipeline: HTTP request → HTML parsing → 
    content cleaning → markdown conversion → metadata extraction. It's designed to work with URLs
    from search results, business websites, news articles, and other web sources.

    The tool automatically removes noise elements (ads, navigation, tracking scripts) and extracts
    the main content, making it much easier for AI to understand and analyze web page information.

    Example workflow integration:
        1. Use generate_search_url to create search URLs
        2. Use this tool to process search result pages
        3. Extract business website URLs from the results
        4. Use this tool again to process business websites for contact info
        5. Use file_write to save findings for future reference

    Example response for successful processing:
        {
            "status": "success",
            "url": "https://company.com/about",
            "title": "About Us - Company Name",
            "description": "Learn about our company history and mission",
            "content": "# About Company Name\n\nWe are a leading provider of...\n\n## Contact Information\n\nEmail: info@company.com\nPhone: (555) 123-4567",
            "word_count": 847
        }

    When to use this tool:
        - Processing search engine result pages to find relevant links
        - Extracting content from business websites for contact information
        - Converting news articles or blog posts to readable format
        - Analyzing competitor websites for research
        - Processing any web page that contains information you need to analyze

    What this tool handles automatically:
        - Removes ads, navigation menus, sidebars, and footer content
        - Strips out JavaScript, tracking pixels, and analytics code
        - Converts HTML tables, lists, and formatting to clean markdown
        - Extracts page title and meta description for context
        - Handles redirects and follows canonical URLs
        - Provides detailed error reporting for blocked or failed requests

    Limitations and modern web challenges:
        - Many sites now use anti-bot protection (CloudFlare, reCAPTCHA, etc.)
        - JavaScript-heavy sites may not render complete content
        - Some sites may return different content to automated requests
        - Rate limiting may block rapid successive requests
        - Results marked as "blocked" require manual verification

    Args:
        url: The web page URL to process and extract content from (string)
             Must be a valid HTTP or HTTPS URL
             Example: "https://www.company.com/contact" or "https://news.site.com/article"
        timeout: Maximum time to wait for the web request in seconds (integer)
                Default: 30 seconds, recommended range: 10-60 seconds
                Higher values for slow-loading pages, lower for quick checks

    Returns:
        Dictionary containing the processing results and extracted content:
        
        On success (status="success"):
        - status: "success" (string)
        - url: Final URL after any redirects (string)
        - title: Page title extracted from HTML <title> tag (string)
        - description: Meta description from <meta name="description"> (string)
        - content: Clean markdown content with main page information (string)
        - word_count: Number of words in the processed content (integer)
        - original_length: Size of raw HTML in characters (integer)
        - processed_length: Size of cleaned markdown in characters (integer)

        On error (status="error" or "blocked"):
        - status: "error" or "blocked" (string)
        - url: The requested URL (string)
        - error: Description of what went wrong (string)
        - suggestion: Recommended next steps for manual verification (string, if blocked)
        - content: None
    """
    logger.info(f"process_web_content called: url='{url}', timeout={timeout}")
    
    async def _crawl_with_browser():
        """Internal async function to handle Crawl4AI browser automation"""
        try:
            # Configure browser without stealth mode due to import issues
            browser_config = BrowserConfig(
                enable_stealth=False,
                headless=True,
                verbose=False
            )
            
            logger.info(f"Starting Crawl4AI browser for: {url}")
            
            async with AsyncWebCrawler(
                config=browser_config
            ) as crawler:
                result = await crawler.arun(
                    url=url,
                    page_timeout=timeout * 1000,  # Convert to milliseconds
                    wait_for_images=False,
                    process_iframes=False,
                    remove_overlay_elements=True
                )
                
                if result.success:
                    logger.info(f"Successfully crawled {url}, markdown length: {len(result.markdown)}")
                    # Return clean markdown with basic formatting
                    markdown_result = f"**Web Content from {result.url}**\n\n"
                    
                    if result.metadata and result.metadata.get('title'):
                        markdown_result += f"**Title**: {result.metadata['title']}\n\n"
                    
                    markdown_result += result.markdown
                    
                    return markdown_result
                else:
                    logger.error(f"Crawl4AI failed for {url}: {result.error_message}")
                    return f"**Error**: Failed to crawl {url} - {result.error_message}"
                    
        except Exception as e:
            logger.error(f"Crawl4AI error for {url}: {str(e)}")
            return f"**Error**: Browser crawling failed for {url} - {str(e)}"
    
    # Run the async crawling function
    try:
        return asyncio.run(_crawl_with_browser())
    except Exception as e:
        logger.error(f"Async execution error for {url}: {str(e)}")
        return f"**Error**: Execution failed for {url} - {str(e)}"


# Official strands_tools are now used for:
# - file_read: Read files and configuration data
# - file_write: Save research results and reports  
# - current_time: Timestamp research activities
#
# Custom tools specific to QuickResearch_Quinten implemented above:
# - generate_search_url: Create Google search URLs
# - process_web_content: Complete URL-to-markdown pipeline

# Export custom functions
__all__ = ['generate_search_url', 'process_web_content']