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
    """Generate search URLs for web research tasks.

    Creates properly formatted search engine URLs optimized for automated access.
    DuckDuckGo is recommended for better bot detection avoidance.

    Args:
        engine: Search engine to use. Options: "duckduckgo", "bing", "google".
                Recommended: "duckduckgo"
        keywords: Search terms as list of strings. Must contain at least one term.
                 Example: ["Python", "tutorial"] or ["company", "contact"]

    Returns:
        str: URL-encoded search URL ready for web scraping
    
    Raises:
        ValueError: If keywords list is empty or engine is unsupported
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
    """Extract clean, readable content from web pages using browser automation.

    Processes web pages through complete pipeline: HTTP request → HTML parsing → 
    content cleaning → markdown conversion. Removes ads, navigation, and tracking 
    elements to provide clean content for analysis.

    Uses Crawl4AI browser automation to handle modern websites with JavaScript
    and anti-bot protection. Automatically converts HTML to structured markdown.

    Common workflow:
        1. generate_search_url() → create search URLs
        2. process_web_content() → process search results  
        3. extract_urls_from_content() → find target URLs
        4. process_web_content() → extract target content
        5. extract_contact_info() → parse contact details

    Args:
        url: Valid HTTP/HTTPS URL to process.
             Example: "https://company.com/contact"
        timeout: Request timeout in seconds. Default: 30, range: 10-60

    Returns:
        str: Formatted markdown content with title and extracted text.
             Returns error message string if processing fails.

    Note:
        Modern websites may use anti-bot protection (CloudFlare, reCAPTCHA).
        JavaScript-heavy sites may not render complete content.
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
    """Extract and validate URLs from web content using regex patterns.

    Reliably finds URLs in messy HTML/markdown content where LLMs struggle with
    precise extraction. Handles multiple URL formats and validates results.

    Args:
        content: Text/markdown content to parse for URLs
        domain_filter: Optional domain substring to filter results.
                      Example: ".com", "facebook", "linkedin"

    Returns:
        str: Formatted numbered list of extracted URLs.
             Returns "No URLs found" message if none match criteria.
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
    """Extract structured contact information using specialized regex patterns.

    Reliably finds emails, phone numbers, addresses, and social media links
    where LLMs struggle with precise pattern matching.

    Args:
        content: Text/markdown content to parse for contact details

    Returns:
        str: Formatted contact information grouped by type (emails, phones, 
             addresses, social media). Returns "No contact information found"
             if none detected.
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


# Export custom functions
__all__ = ['generate_search_url', 'process_web_content', 'extract_urls_from_content', 'extract_contact_info']