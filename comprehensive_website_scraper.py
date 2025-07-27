"""
Comprehensive Website Scraper with Markdown and JSON Output

This script combines all the functionality from the other scripts to provide a complete
website scraping solution with multiple output formats and strategies.

Features:
- Multiple output formats: Markdown, JSON, and Raw HTML
- Multiple extraction strategies: Simple, LLM-based, and Custom
- Batch processing for multiple websites
- Configurable crawling parameters
- Error handling and logging
- Progress tracking and reporting
"""

import asyncio
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
from pathlib import Path
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai.chunking_strategy import ChunkingStrategy

# Load environment variables
load_dotenv('config.env')

class ComprehensiveWebsiteScraper:
    def __init__(self, api_key: Optional[str] = None, output_dir: str = "scraped_data"):
        """Initialize the comprehensive website scraper"""
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self.model = os.getenv('DEFAULT_MODEL', 'meta-llama/llama-3.3-70b-instruct:free')
        
        if not self.api_key:
            raise ValueError("Please set OPENROUTER_API_KEY in config.env file or pass it to the constructor")
        
        self.llm_config = self._get_llm_config()
        self.output_dir = output_dir
        
        # Create output directory
        Path(self.output_dir).mkdir(exist_ok=True)
    
    def _get_llm_config(self) -> Dict[str, Any]:
        """Configure LLM settings for OpenRouter"""
        return {
            "provider": "openai",
            "api_key": self.api_key,
            "base_url": self.base_url,
            "model": self.model,
            "temperature": 0.1,
            "max_tokens": 4000,
            "headers": {
                "HTTP-Referer": "https://github.com/crawl4ai-integration",
                "X-Title": "Comprehensive Website Scraper"
            }
        }
    
    def _get_extraction_prompt(self, url: str) -> str:
        """Generate a comprehensive extraction prompt for the given URL"""
        domain = urlparse(url).netloc
        
        return f"""
        Extract comprehensive information from this webpage and return it as a structured JSON object.
        
        Website: {url}
        Domain: {domain}
        
        Please extract the following information and format it as valid JSON:
        
        {{
            "metadata": {{
                "url": "the original URL",
                "title": "page title",
                "description": "meta description or main page description",
                "language": "detected language",
                "last_updated": "if available",
                "word_count": "approximate word count"
            }},
            "content": {{
                "main_heading": "main page heading",
                "sub_headings": ["list of sub-headings"],
                "main_content": "main text content (summarized)",
                "key_points": ["list of key points or features"],
                "call_to_actions": ["list of buttons, links, or CTAs"]
            }},
            "navigation": {{
                "menu_items": ["list of navigation menu items"],
                "breadcrumbs": ["breadcrumb navigation if available"],
                "footer_links": ["list of footer links"]
            }},
            "media": {{
                "images": ["list of image descriptions or alt texts"],
                "videos": ["list of video titles or descriptions"],
                "documents": ["list of downloadable documents"]
            }},
            "business_info": {{
                "company_name": "if available",
                "contact_info": {{
                    "email": "email addresses",
                    "phone": "phone numbers",
                    "address": "physical addresses"
                }},
                "social_media": ["social media links"],
                "pricing": "pricing information if available"
            }},
            "technical": {{
                "technologies": ["detected technologies or frameworks"],
                "forms": ["list of forms and their purposes"],
                "external_links": ["list of external links"]
            }}
        }}
        
        Important:
        - Return ONLY valid JSON, no additional text
        - Use null for missing information
        - Keep text concise but informative
        - Preserve the exact structure above
        - If information is not available, use null or empty arrays/objects
        """
    
    async def scrape_website(
        self, 
        url: str, 
        strategy: str = "comprehensive",
        output_formats: List[str] = ["markdown", "json"],
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Scrape a website using the specified strategy and output formats
        
        Args:
            url: The website URL to scrape
            strategy: Scraping strategy ("simple", "llm", "comprehensive")
            output_formats: List of output formats ("markdown", "json", "html", "raw")
            custom_prompt: Custom extraction prompt for LLM strategy
            
        Returns:
            Dictionary containing the scraped data and results
        """
        valid_formats = ["markdown", "json", "html", "raw"]
        output_formats = [fmt for fmt in output_formats if fmt in valid_formats]
        if not output_formats:
            print(f"⚠️ No valid output formats provided, defaulting to {valid_formats}")
            output_formats = valid_formats
        
        print(f"🕷️ Starting {strategy} scrape of: {url}")
        
        try:
            if strategy not in ["simple", "llm", "comprehensive"]:
                raise ValueError(f"Unknown strategy: {strategy}")
            
            extraction_strategy = None
            chunking_strategy = None
            if strategy == "llm":
                extraction_strategy = LLMExtractionStrategy(
                    llm_config=self.llm_config,
                    extraction_prompt=custom_prompt or self._get_extraction_prompt(url)
                )
            elif strategy == "comprehensive":
                extraction_strategy = LLMExtractionStrategy(
                    llm_config=self.llm_config,
                    extraction_prompt=custom_prompt or self._get_extraction_prompt(url)
                )
                # For now, skip chunking strategy as it's causing issues
                chunking_strategy = None
            
            async with AsyncWebCrawler() as crawler:
                print(f"📡 Crawling website using {strategy} strategy...")  # Fixed f-string
                result = await crawler.arun(
                    url=url,
                    extraction_strategy=extraction_strategy,
                    chunking_strategy=chunking_strategy,
                    llm_config=self.llm_config if strategy != "simple" else None,
                    wait_for="networkidle",
                    timeout=30000,
                    max_retries=3
                )
                
                print("✅ Crawling completed!")
                print(f"📄 Raw content length: {len(result.markdown)} characters")
                print(f"🔗 Links found: {len(result.links)}")
                
                processed_data = self._process_results(result, url, strategy, output_formats)
                saved_files = self._save_outputs(processed_data, url, output_formats)
                
                return {
                    "success": True,
                    "url": url,
                    "strategy": strategy,
                    "output_formats": output_formats,
                    "data": processed_data,
                    "saved_files": saved_files,
                    "metadata": {
                        "scraped_at": datetime.now().isoformat(),
                        "crawler_version": "Crawl4AI + OpenRouter LLM",
                        "model_used": self.model if strategy != "simple" else "none",
                        "raw_content_length": len(result.markdown),
                        "links_found": len(result.links),
                        "chunks_processed": len(result.chunks) if hasattr(result, 'chunks') else 0
                    }
                }
                
        except Exception as e:
            error_data = {
                "success": False,
                "error": {
                    "message": str(e),
                    "type": type(e).__name__,
                    "url": url,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            print(f"❌ Error scraping {url}: {e}")
            return error_data
    
    def _process_results(self, result, url: str, strategy: str, output_formats: List[str]) -> Dict[str, Any]:
        """Process the crawler results based on output formats"""
        processed_data = {
            "basic_info": {
                "url": url,
                "strategy": strategy,
                "content_length": len(result.markdown),
                "links_count": len(result.links),
                "scraped_at": datetime.now().isoformat()
            }
        }
        
        if "markdown" in output_formats:
            processed_data["markdown"] = result.markdown
        
        if "html" in output_formats and hasattr(result, 'html'):
            processed_data["html"] = result.html
        
        if "json" in output_formats:
            processed_data["json"] = (self._create_simple_json_structure(result, url) if strategy == "simple"
                                    else self._parse_extracted_content(result, url))
        
        if "raw" in output_formats:
            processed_data["raw"] = {
                "markdown": result.markdown,
                "links": list(result.links) if result.links else [],
                "metadata": result.__dict__ if hasattr(result, '__dict__') else {}
            }
        
        return processed_data
    
    def _parse_extracted_content(self, result, url: str) -> Dict[str, Any]:
        """Parse the extracted content from the crawler result"""
        try:
            if hasattr(result, 'extracted_content') and result.extracted_content:
                content_str = str(result.extracted_content).strip()
                
                if content_str.startswith('```json'):
                    content_str = content_str[7:-3] if content_str.endswith('```') else content_str[7:]
                
                parsed_data = json.loads(content_str)
                parsed_data["raw_markdown"] = result.markdown[:1000] + "..." if len(result.markdown) > 1000 else result.markdown
                return parsed_data
            return self._create_fallback_structure(result, url)
                
        except json.JSONDecodeError as e:
            print(f"⚠️ Could not parse extracted content as JSON: {e}")
            print("📝 Using fallback structure...")
            return self._create_fallback_structure(result, url)
    
    def _create_simple_json_structure(self, result, url: str) -> Dict[str, Any]:
        """Create a simple JSON structure for basic scraping"""
        domain = urlparse(url).netloc
        
        return {
            "metadata": {
                "url": url,
                "title": f"Content from {domain}",
                "description": "Basic scraping result",
                "language": "unknown",
                "word_count": len(result.markdown.split())
            },
            "content": {
                "main_content": result.markdown[:1000] + "..." if len(result.markdown) > 1000 else result.markdown,
                "full_content": result.markdown
            },
            "links": list(result.links)[:20] if result.links else [],
            "scraping_method": "simple"
        }
    
    def _create_fallback_structure(self, result, url: str) -> Dict[str, Any]:
        """Create a fallback structure when JSON parsing fails"""
        domain = urlparse(url).netloc
        
        return {
            "metadata": {
                "url": url,
                "title": "Extracted from markdown",
                "description": "Content extracted using fallback method",
                "language": "unknown",
                "last_updated": None,
                "word_count": len(result.markdown.split())
            },
            "content": {
                "main_heading": "Content from " + domain,
                "sub_headings": [],
                "main_content": result.markdown[:500] + "..." if len(result.markdown) > 500 else result.markdown,
                "key_points": [],
                "call_to_actions": []
            },
            "navigation": {
                "menu_items": [],
                "breadcrumbs": [],
                "footer_links": list(result.links)[:10] if result.links else []
            },
            "media": {
                "images": [],
                "videos": [],
                "documents": []
            },
            "business_info": {
                "company_name": domain,
                "contact_info": {
                    "email": None,
                    "phone": None,
                    "address": None
                },
                "social_media": [],
                "pricing": None
            },
            "technical": {
                "technologies": [],
                "forms": [],
                "external_links": list(result.links)[:10] if result.links else []
            },
            "raw_markdown": result.markdown,
            "extraction_method": "fallback"
        }
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path injection or invalid characters"""
        return re.sub(r'[^\w\-_\.]', '_', filename)
    
    def _save_outputs(self, processed_data: Dict[str, Any], url: str, output_formats: List[str]) -> Dict[str, str]:
        """Save the processed data to files"""
        saved_files = {}
        domain = self._sanitize_filename(urlparse(url).netloc)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            if "markdown" in output_formats and "markdown" in processed_data:
                markdown_file = f"{self.output_dir}/{domain}_{timestamp}.md"
                with open(markdown_file, 'w', encoding='utf-8') as f:
                    f.write(processed_data["markdown"])
                saved_files["markdown"] = markdown_file
                print(f"💾 Markdown saved to: {markdown_file}")
            
            if "json" in output_formats and "json" in processed_data:
                json_file = f"{self.output_dir}/{domain}_{timestamp}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(processed_data["json"], f, indent=2, ensure_ascii=False)
                saved_files["json"] = json_file
                print(f"💾 JSON saved to: {json_file}")
            
            if "html" in output_formats and "html" in processed_data:
                html_file = f"{self.output_dir}/{domain}_{timestamp}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(processed_data["html"])
                saved_files["html"] = html_file
                print(f"💾 HTML saved to: {html_file}")
            
            if "raw" in output_formats and "raw" in processed_data:
                raw_file = f"{self.output_dir}/{domain}_{timestamp}_raw.json"
                with open(raw_file, 'w', encoding='utf-8') as f:
                    json.dump(processed_data["raw"], f, indent=2, ensure_ascii=False)
                saved_files["raw"] = raw_file
                print(f"💾 Raw data saved to: {raw_file}")
            
        except Exception as e:
            print(f"❌ Error saving files: {e}")
        
        return saved_files
    
    async def scrape_multiple_websites(
        self, 
        urls: List[str], 
        strategy: str = "comprehensive",
        output_formats: List[str] = ["markdown", "json"],
        delay: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Scrape multiple websites with specified strategy and output formats
        
        Args:
            urls: List of website URLs to scrape
            strategy: Scraping strategy for all websites
            output_formats: Output formats for all websites
            delay: Delay between requests in seconds
            
        Returns:
            List of scraping results
        """
        print(f"🚀 Starting batch scrape of {len(urls)} websites...")
        print(f"📊 Strategy: {strategy}")
        print(f"📄 Output formats: {', '.join(output_formats)}")
        
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n📊 Progress: {i}/{len(urls)} - {url}")
            
            result = await self.scrape_website(url, strategy, output_formats)
            results.append(result)
            
            if i < len(urls):
                print(f"⏳ Waiting {delay} seconds before next request...")
                await asyncio.sleep(delay)
        
        summary = self._generate_summary_report(results)
        summary_file = f"{self.output_dir}/scraping_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Batch scraping completed!")
        print(f"📁 Results saved to: {self.output_dir}/")
        print(f"📊 Summary saved to: {summary_file}")
        
        return results
    
    def _generate_summary_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary report of the scraping results"""
        successful = [r for r in results if r.get("success", False)]
        failed = [r for r in results if not r.get("success", False)]
        
        return {
            "summary": {
                "total_websites": len(results),
                "successful": len(successful),
                "failed": len(failed),
                "success_rate": f"{(len(successful) / len(results) * 100):.1f}%" if results else "0%"
            },
            "successful_urls": [r.get("url", "unknown") for r in successful if isinstance(r, dict)],
            "failed_urls": [r.get("url", "unknown") for r in failed if isinstance(r, dict)],
            "errors": [r.get("error", {}).get("message", "Unknown error") for r in failed if isinstance(r, dict)],
            "generated_at": datetime.now().isoformat()
        }