"""
Main Usage Example for Comprehensive Website Scraper

This is the main usage file that demonstrates different scraping strategies
and output formats using a single target URL. All functions share the same
target URL for easy comparison and testing.

Features:
- Single target URL for all examples
- Modular functions for different use cases
- Multiple output formats demonstration
- Different scraping strategies
- Easy to customize and extend
"""

import asyncio
import json
from comprehensive_website_scraper import ComprehensiveWebsiteScraper

# Global configuration - Change this URL to test different websites
TARGET_URL = "https://crawl4ai.com"

# Output directory for all results
OUTPUT_DIR = "scraping_results"

async def simple_scraping_example():
    """Example 1: Simple scraping without LLM (fastest)"""
    print(f"\n1️⃣ Simple Scraping Example")
    print("=" * 50)
    print(f"Target: {TARGET_URL}")
    print("Strategy: Simple (no LLM)")
    print("Output: Markdown + JSON")
    
    scraper = ComprehensiveWebsiteScraper()
    
    result = await scraper.scrape_website(
        url=TARGET_URL,
        strategy="simple",
        output_formats=["markdown", "json"]
    )
    
    if result["success"]:
        print(f"✅ Success! Files saved:")
        for format_type, file_path in result["saved_files"].items():
            print(f"   📄 {format_type.upper()}: {file_path}")
        print(f"📊 Content length: {result['metadata']['raw_content_length']} characters")
    else:
        print(f"❌ Error: {result['error']['message']}")
    
    return result

async def llm_scraping_example():
    """Example 2: LLM-based extraction with custom prompt"""
    print(f"\n2️⃣ LLM Scraping Example")
    print("=" * 50)
    print(f"Target: {TARGET_URL}")
    print("Strategy: LLM-based extraction")
    print("Output: JSON with structured data")
    
    scraper = ComprehensiveWebsiteScraper()
    
    # Custom prompt for specific information extraction
    custom_prompt = """
    Extract the following information from this webpage and return as JSON:
    
    {
        "product_name": "name of the main product or service",
        "description": "brief description of what this website offers",
        "key_features": ["list of main features or capabilities"],
        "target_audience": "who this product is for",
        "pricing_info": "any pricing information available",
        "contact_info": "how to contact or get support"
    }
    
    Return ONLY valid JSON, no additional text.
    """
    
    result = await scraper.scrape_website(
        url=TARGET_URL,
        strategy="llm",
        output_formats=["json"],
        custom_prompt=custom_prompt
    )
    
    if result["success"]:
        print(f"✅ Success! JSON saved to: {result['saved_files']['json']}")
        # Show a preview of the extracted data
        if "json" in result["data"]:
            json_data = result["data"]["json"]
            if isinstance(json_data, dict):
                print("📊 Extracted data preview:")
                for key, value in json_data.items():
                    if isinstance(value, list):
                        print(f"   {key}: {len(value)} items")
                    else:
                        print(f"   {key}: {str(value)[:50]}...")
    else:
        print(f"❌ Error: {result['error']['message']}")
    
    return result

async def comprehensive_scraping_example():
    """Example 3: Comprehensive scraping with all output formats"""
    print(f"\n3️⃣ Comprehensive Scraping Example")
    print("=" * 50)
    print(f"Target: {TARGET_URL}")
    print("Strategy: Comprehensive (LLM + chunking)")
    print("Output: Markdown + JSON + HTML + Raw")
    
    scraper = ComprehensiveWebsiteScraper()
    
    result = await scraper.scrape_website(
        url=TARGET_URL,
        strategy="comprehensive",
        output_formats=["markdown", "json", "html", "raw"]
    )
    
    if result["success"]:
        print(f"✅ Success! All formats saved:")
        for format_type, file_path in result["saved_files"].items():
            print(f"   📄 {format_type.upper()}: {file_path}")
        print(f"📊 Processing details:")
        print(f"   - Model used: {result['metadata']['model_used']}")
        print(f"   - Links found: {result['metadata']['links_found']}")
        print(f"   - Chunks processed: {result['metadata']['chunks_processed']}")
    else:
        print(f"❌ Error: {result['error']['message']}")
    
    return result

async def batch_scraping_example():
    """Example 4: Batch scraping multiple related URLs"""
    print(f"\n4️⃣ Batch Scraping Example")
    print("=" * 50)
    print("Target: Multiple related URLs")
    print("Strategy: Comprehensive")
    print("Output: Markdown + JSON for each site")
    
    scraper = ComprehensiveWebsiteScraper()
    
    # Related URLs to the main target
    related_urls = [
        TARGET_URL,
        "https://docs.crawl4ai.com",
        "https://github.com/unclecode/crawl4ai"
    ]
    
    print(f"📋 URLs to scrape:")
    for i, url in enumerate(related_urls, 1):
        print(f"   {i}. {url}")
    
    results = await scraper.scrape_multiple_websites(
        urls=related_urls,
        strategy="comprehensive",
        output_formats=["markdown", "json"],
        delay=2
    )
    
    # Summary
    successful = [r for r in results if r.get("success", False)]
    failed = [r for r in results if not r.get("success", False)]
    
    print(f"\n📊 Batch Scraping Summary:")
    print(f"   ✅ Successful: {len(successful)}/{len(related_urls)}")
    print(f"   ❌ Failed: {len(failed)}")
    print(f"   📁 Results saved to: {scraper.output_dir}/")
    
    if failed:
        print(f"   ⚠️ Failed URLs:")
        for result in failed:
            print(f"      - {result['url']}: {result['error']['message']}")
    
    return results

async def custom_extraction_example():
    """Example 5: Custom extraction with specific data focus"""
    print(f"\n5️⃣ Custom Extraction Example")
    print("=" * 50)
    print(f"Target: {TARGET_URL}")
    print("Strategy: LLM with custom prompt")
    print("Output: JSON with specific data focus")
    
    scraper = ComprehensiveWebsiteScraper()
    
    # Custom prompt focused on technical information
    technical_prompt = """
    Extract technical information from this webpage and return as JSON:
    
    {
        "technologies": ["list of technologies, frameworks, or tools mentioned"],
        "api_endpoints": ["list of API endpoints if any"],
        "installation": "installation or setup instructions",
        "dependencies": ["list of dependencies or requirements"],
        "deployment": "deployment or hosting information",
        "documentation": "links to documentation or guides"
    }
    
    Focus on technical details, code examples, and developer information.
    Return ONLY valid JSON.
    """
    
    result = await scraper.scrape_website(
        url=TARGET_URL,
        strategy="llm",
        output_formats=["json"],
        custom_prompt=technical_prompt
    )
    
    if result["success"]:
        print(f"✅ Success! Technical data saved to: {result['saved_files']['json']}")
        # Show technical data preview
        if "json" in result["data"]:
            json_data = result["data"]["json"]
            if isinstance(json_data, dict):
                print("🔧 Technical data extracted:")
                for key, value in json_data.items():
                    if isinstance(value, list):
                        print(f"   {key}: {len(value)} items")
                        if value:
                            print(f"      Examples: {', '.join(value[:3])}")
                    else:
                        print(f"   {key}: {str(value)[:100]}...")
    else:
        print(f"❌ Error: {result['error']['message']}")
    
    return result

async def run_all_examples():
    """Run all examples sequentially"""
    print("🚀 Comprehensive Website Scraper - All Examples")
    print("=" * 60)
    print(f"🎯 Target URL: {TARGET_URL}")
    print(f"📁 Output Directory: {OUTPUT_DIR}")
    print("=" * 60)
    
    results = {}
    
    # Run all examples
    results["simple"] = await simple_scraping_example()
    results["llm"] = await llm_scraping_example()
    results["comprehensive"] = await comprehensive_scraping_example()
    results["batch"] = await batch_scraping_example()
    results["custom"] = await custom_extraction_example()
    
    # Final summary
    print(f"\n🎉 All Examples Completed!")
    print("=" * 60)
    
    successful_examples = sum(1 for r in results.values() if isinstance(r, dict) and r.get("success", False))
    total_examples = len(results)
    
    print(f"📊 Summary:")
    print(f"   ✅ Successful examples: {successful_examples}/{total_examples}")
    print(f"   📁 All results saved to: {OUTPUT_DIR}/")
    print(f"   🎯 Target URL tested: {TARGET_URL}")
    
    return results

async def run_single_example(example_name: str):
    """Run a single example by name"""
    examples = {
        "simple": simple_scraping_example,
        "llm": llm_scraping_example,
        "comprehensive": comprehensive_scraping_example,
        "batch": batch_scraping_example,
        "custom": custom_extraction_example
    }
    
    if example_name not in examples:
        print(f"❌ Unknown example: {example_name}")
        print(f"Available examples: {', '.join(examples.keys())}")
        return None
    
    print(f"🎯 Running example: {example_name}")
    return await examples[example_name]()

if __name__ == "__main__":
    import sys
    
    # Check if a specific example was requested
    if len(sys.argv) > 1:
        example_name = sys.argv[1].lower()
        asyncio.run(run_single_example(example_name))
    else:
        # Run all examples
        asyncio.run(run_all_examples()) 