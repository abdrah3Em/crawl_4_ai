"""
Main Usage task for Comprehensive Website Scraper

This is the main usage file that demonstrates different scraping strategies
and output formats using a single target URL. All functions share the same
target URL for easy comparison and testing.

Features:
- Single target URL for all tasks
- Modular functions for different use cases
- Multiple output formats demonstration
- Different scraping strategies
- Easy to customize and extend
"""

import asyncio
import json
import sys
from comprehensive_website_scraper import ComprehensiveWebsiteScraper  # Added explicit import

# Global configuration - Change this URL to test different websites
TARGET_URL = "https://rscolman.com.ng/"

# Output directory for all results
OUTPUT_DIR = "scraped_data"  # Aligned with scraper class

# Universal output format configuration
# Options: "json", "markdown", "both", "all"
# - "json": Only JSON output
# - "markdown": Only markdown output  
# - "both": Both JSON and markdown
# - "all": All formats (JSON, markdown, HTML, raw)
OUTPUT_FORMAT = "json"

def get_output_formats(output_format: str) -> list:
    """Convert universal output format to list of formats"""
    format_mapping = {
        "json": ["json"],
        "markdown": ["markdown"],
        "both": ["markdown", "json"],
        "all": ["markdown", "json", "html", "raw"]
    }
    
    if output_format not in format_mapping:
        print(f"⚠️ Unknown output format '{output_format}', using 'both'")
        return format_mapping["both"]
    
    return format_mapping[output_format]

async def simple_scraping_task():
    """Task 1: Simple scraping without LLM (fastest)"""
    print(f"\n1️⃣ Simple Scraping task")
    print("=" * 50)
    print(f"Target: {TARGET_URL}")
    print("Strategy: Simple (no LLM)")
    print(f"Output: {OUTPUT_FORMAT}")
    
    scraper = ComprehensiveWebsiteScraper(output_dir=OUTPUT_DIR)  # Pass output_dir
    
    output_formats = get_output_formats(OUTPUT_FORMAT)
    
    result = await scraper.scrape_website(
        url=TARGET_URL,
        strategy="simple",
        output_formats=output_formats
    )
    
    if result["success"]:
        print(f"✅ Success! Files saved:")
        for format_type, file_path in result["saved_files"].items():
            print(f"   📄 {format_type.upper()}: {file_path}")
        print(f"📊 Content length: {result['metadata']['raw_content_length']} characters")
    else:
        print(f"❌ Error: {result['error']['message']}")
    
    return result

async def llm_scraping_task():
    """Task 2: LLM-based extraction with custom prompt"""
    print(f"\n2️⃣ LLM Scraping task")
    print("=" * 50)
    print(f"Target: {TARGET_URL}")
    print("Strategy: LLM-based extraction")
    print(f"Output: {OUTPUT_FORMAT}")
    
    scraper = ComprehensiveWebsiteScraper(output_dir=OUTPUT_DIR)
    
    output_formats = get_output_formats(OUTPUT_FORMAT)
    
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
        output_formats=output_formats,
        custom_prompt=custom_prompt
    )
    
    if result["success"]:
        print(f"✅ Success! JSON saved to: {result['saved_files']['json']}")
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

async def comprehensive_scraping_task():
    """Task 3: Comprehensive scraping with all output formats"""
    print(f"\n3️⃣ Comprehensive Scraping task")
    print("=" * 50)
    print(f"Target: {TARGET_URL}")
    print("Strategy: Comprehensive (LLM + chunking)")
    print(f"Output: {OUTPUT_FORMAT}")
    
    scraper = ComprehensiveWebsiteScraper(output_dir=OUTPUT_DIR)
    
    output_formats = get_output_formats(OUTPUT_FORMAT)
    
    result = await scraper.scrape_website(
        url=TARGET_URL,
        strategy="comprehensive",
        output_formats=output_formats
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

async def batch_scraping_task():
    """Task 4: Batch scraping multiple related URLs"""
    print(f"\n4️⃣ Batch Scraping task")
    print("=" * 50)
    print("Target: Multiple related URLs")
    print("Strategy: Comprehensive")
    print(f"Output: {OUTPUT_FORMAT}")
    
    scraper = ComprehensiveWebsiteScraper(output_dir=OUTPUT_DIR)
    
    output_formats = get_output_formats(OUTPUT_FORMAT)
    
    # Use only the target URL for simplicity
    related_urls = [TARGET_URL]  # Focus on TARGET_URL
    
    print(f"📋 URLs to scrape:")
    for i, url in enumerate(related_urls, 1):
        print(f"   {i}. {url}")
    
    results = await scraper.scrape_multiple_websites(
        urls=related_urls,
        strategy="comprehensive",
        output_formats=output_formats,
        delay=2
    )
    
    successful = [r for r in results if r.get("success", False)]
    failed = [r for r in results if not r.get("success", False)]
    
    print(f"\n📊 Batch Scraping Summary:")
    print(f"   ✅ Successful: {len(successful)}/{len(related_urls)}")
    print(f"   ❌ Failed: {len(failed)}")
    print(f"   📁 Results saved to: {scraper.output_dir}/")
    
    if failed:
        print(f"   ⚠️ Failed URLs:")
        for result in failed:
            if isinstance(result, dict) and 'url' in result and 'error' in result:
                print(f"      - {result['url']}: {result['error']['message']}")
            else:
                print(f"      - Unknown error in result")
    
    return results

async def custom_extraction_task():
    """Task 5: Custom extraction with specific data focus"""
    print(f"\n5️⃣ Custom Extraction task")
    print("=" * 50)
    print(f"Target: {TARGET_URL}")
    print("Strategy: LLM with custom prompt")
    print(f"Output: {OUTPUT_FORMAT}")
    
    scraper = ComprehensiveWebsiteScraper(output_dir=OUTPUT_DIR)
    
    output_formats = get_output_formats(OUTPUT_FORMAT)
    
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
    
    Focus on technical details, code tasks, and developer information.
    Return ONLY valid JSON.
    """
    
    result = await scraper.scrape_website(
        url=TARGET_URL,
        strategy="llm",
        output_formats=output_formats,
        custom_prompt=technical_prompt
    )
    
    if result["success"]:
        print(f"✅ Success! Technical data saved to: {result['saved_files']['json']}")
        if "json" in result["data"]:
            json_data = result["data"]["json"]
            if isinstance(json_data, dict):
                print("🔧 Technical data extracted:")
                for key, value in json_data.items():
                    if isinstance(value, list):
                        print(f"   {key}: {len(value)} items")
                        if value:
                            print(f"      tasks: {', '.join(value[:3])}")
                    else:
                        print(f"   {key}: {str(value)[:100]}...")
    else:
        print(f"❌ Error: {result['error']['message']}")
    
    return result

async def run_all_tasks():
    """Run all tasks sequentially"""
    print("🚀 Comprehensive Website Scraper - All tasks")
    print("=" * 60)
    print(f"🎯 Target URL: {TARGET_URL}")
    print(f"📁 Output Directory: {OUTPUT_DIR}")
    print(f"📄 Output Format: {OUTPUT_FORMAT}")
    print("=" * 60)
    
    results = {}
    
    try:
        results["simple"] = await simple_scraping_task()
        results["llm"] = await llm_scraping_task()
        results["comprehensive"] = await comprehensive_scraping_task()
        results["batch"] = await batch_scraping_task()
        results["custom"] = await custom_extraction_task()
        
        print(f"\n🎉 All tasks completed!")
        print("=" * 60)
        
        successful_tasks = sum(1 for r in results.values() if isinstance(r, dict) and r.get("success", False))
        total_tasks = len(results)
        
        print(f"📊 Summary:")
        print(f"   ✅ Successful tasks: {successful_tasks}/{total_tasks}")
        print(f"   📁 All results saved to: {OUTPUT_DIR}/")
        print(f"   🎯 Target URL tested: {TARGET_URL}")
    
    except Exception as e:
        print(f"❌ Error running tasks: {e}")
    
    return results

async def run_single_task(task_name: str):
    """Run a single task by name"""
    tasks = {
        "simple": simple_scraping_task,
        "llm": llm_scraping_task,
        "comprehensive": comprehensive_scraping_task,
        "batch": batch_scraping_task,
        "custom": custom_extraction_task
    }
    
    if task_name not in tasks:
        print(f"❌ Unknown task: {task_name}")
        print(f"Available tasks: {', '.join(tasks.keys())}")
        return None
    
    print(f"🎯 Running task: {task_name}")
    try:
        return await tasks[task_name]()
    except Exception as e:
        print(f"❌ Error running task {task_name}: {e}")
        return None

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            task_name = sys.argv[1].lower()
            asyncio.run(run_single_task(task_name))
        else:
            asyncio.run(run_all_tasks())
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)