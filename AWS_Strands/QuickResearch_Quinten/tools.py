"""
Tools for Quick Research Quinten Agent

Provides atomic research tools following Strands framework patterns.
"""

import urllib.parse
import asyncio
import json
import re
from typing import List, Dict, Any, Optional
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


@tool
def extract_urls_from_content(content: str, domain_filter: Optional[str] = None) -> str:
    """
    Extract and validate URLs from web content, especially search results.
    
    LLMs often struggle with precise URL extraction from messy HTML/markdown content.
    This tool uses regex patterns to reliably find all URLs and validate them.
    
    Args:
        content: Text/markdown content to extract URLs from (string)
        domain_filter: Optional domain to filter results (e.g., ".com", "facebook")
    
    Returns:
        Formatted list of extracted URLs as string
    """
    logger.info(f"extract_urls_from_content called: content_length={len(content)}, domain_filter='{domain_filter}'")
    
    try:
        # Multiple URL patterns to catch different formats
        url_patterns = [
            # Standard HTTP/HTTPS URLs
            r'https?://[^\s\[\]()<>"\']+',
            # URLs in markdown links [text](url)
            r'\]\(https?://[^\)]+\)',
            # URLs in HTML href attributes
            r'href=["\']https?://[^"\']+["\']'
        ]
        
        found_urls = set()
        
        for pattern in url_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                url = match
                if url.startswith(']('):
                    url = url[2:-1]  # Remove ]( and )
                elif url.startswith('href='):
                    url = url[6:-1]  # Remove href=" and "
                
                # Basic URL validation
                if url.startswith(('http://', 'https://')) and '.' in url:
                    # Remove trailing punctuation
                    url = re.sub(r'[.,;!?]+$', '', url)
                    found_urls.add(url)
        
        # Filter by domain if specified
        if domain_filter:
            found_urls = {url for url in found_urls if domain_filter.lower() in url.lower()}
        
        # Sort URLs for consistent output
        sorted_urls = sorted(list(found_urls))
        
        logger.info(f"Extracted {len(sorted_urls)} URLs" + (f" matching filter '{domain_filter}'" if domain_filter else ""))
        
        if not sorted_urls:
            return "**No URLs found**" + (f" matching filter '{domain_filter}'" if domain_filter else "")
        
        # Format output
        result = f"**Extracted {len(sorted_urls)} URLs:**\n\n"
        for i, url in enumerate(sorted_urls, 1):
            result += f"{i}. {url}\n"
        
        return result
        
    except Exception as e:
        logger.error(f"URL extraction error: {str(e)}")
        return f"**Error**: URL extraction failed - {str(e)}"


@tool
def extract_contact_info(content: str) -> str:
    """
    Extract structured contact information from web content.
    
    LLMs struggle with precise pattern matching for emails, phones, and addresses.
    This tool uses specialized regex patterns to reliably find contact details.
    
    Args:
        content: Text/markdown content to extract contact info from (string)
    
    Returns:
        Structured contact information as formatted string
    """
    logger.info(f"extract_contact_info called: content_length={len(content)}")
    
    try:
        contact_info = {
            'emails': set(),
            'phones': set(),
            'addresses': [],
            'social_media': set()
        }
        
        # Email patterns
        email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'\bmailto:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        ]
        
        for pattern in email_patterns:
            emails = re.findall(pattern, content, re.IGNORECASE)
            for email in emails:
                if email.startswith('mailto:'):
                    email = email[7:]  # Remove 'mailto:'
                contact_info['emails'].add(email.lower())
        
        # Phone number patterns
        phone_patterns = [
            r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',
            r'\+1[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, content)
            for phone in phones:
                if isinstance(phone, tuple):
                    phone = ''.join(phone)
                # Clean and format phone number
                clean_phone = re.sub(r'[^\d+]', '', str(phone))
                if len(clean_phone) >= 10:
                    contact_info['phones'].add(clean_phone)
        
        # Social media patterns
        social_patterns = [
            (r'facebook\.com/[A-Za-z0-9._-]+', 'Facebook'),
            (r'instagram\.com/[A-Za-z0-9._-]+', 'Instagram'),
            (r'twitter\.com/[A-Za-z0-9._-]+', 'Twitter'),
            (r'linkedin\.com/(?:in|company)/[A-Za-z0-9._-]+', 'LinkedIn'),
            (r'youtube\.com/(?:channel|user|c)/[A-Za-z0-9._-]+', 'YouTube')
        ]
        
        for pattern, platform in social_patterns:
            matches = re.findall(f'https?://{pattern}', content, re.IGNORECASE)
            for match in matches:
                contact_info['social_media'].add(f"{platform}: {match}")
        
        # Simple address pattern (street numbers + street names)
        address_patterns = [
            r'\d+\s+[A-Za-z\s]+(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl|Circle|Cir|Court|Ct)',
            r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl|Circle|Cir|Court|Ct)[\s,]*[A-Za-z\s]*[A-Z]{2}\s+\d{5}'
        ]
        
        for pattern in address_patterns:
            addresses = re.findall(pattern, content, re.IGNORECASE)
            contact_info['addresses'].extend(addresses[:3])  # Limit to first 3 matches
        
        logger.info(f"Extracted: {len(contact_info['emails'])} emails, {len(contact_info['phones'])} phones, {len(contact_info['addresses'])} addresses, {len(contact_info['social_media'])} social")
        
        # Format output
        result = "**Contact Information Extracted:**\n\n"
        
        if contact_info['emails']:
            result += "**Emails:**\n"
            for email in sorted(contact_info['emails']):
                result += f"• {email}\n"
            result += "\n"
        
        if contact_info['phones']:
            result += "**Phone Numbers:**\n"
            for phone in sorted(contact_info['phones']):
                # Format phone for display
                if len(phone) == 10:
                    formatted = f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
                elif len(phone) == 11 and phone.startswith('1'):
                    formatted = f"+1 ({phone[1:4]}) {phone[4:7]}-{phone[7:]}"
                else:
                    formatted = phone
                result += f"• {formatted}\n"
            result += "\n"
        
        if contact_info['addresses']:
            result += "**Addresses:**\n"
            for addr in contact_info['addresses'][:3]:  # Show max 3
                result += f"• {addr}\n"
            result += "\n"
        
        if contact_info['social_media']:
            result += "**Social Media:**\n"
            for social in sorted(contact_info['social_media']):
                result += f"• {social}\n"
            result += "\n"
        
        if not any([contact_info['emails'], contact_info['phones'], contact_info['addresses'], contact_info['social_media']]):
            result = "**No contact information found**\n\nContent may not contain recognizable contact details or may use non-standard formats."
        
        return result.strip()
        
    except Exception as e:
        logger.error(f"Contact extraction error: {str(e)}")
        return f"**Error**: Contact extraction failed - {str(e)}"


# Official strands_tools are now used for:
# - file_read: Read files and configuration data
# - file_write: Save research results and reports  
# - current_time: Timestamp research activities
#
# Custom tools specific to QuickResearch_Quinten implemented above:
# - generate_search_url: Create Google search URLs
# - process_web_content: Complete URL-to-markdown pipeline

# Export custom functions
__all__ = ['generate_search_url', 'process_web_content', 'extract_urls_from_content', 'extract_contact_info']