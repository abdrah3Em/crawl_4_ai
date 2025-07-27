# Crawl4AI with OpenRouter LLM Integration

This project demonstrates how to set up and use [Crawl4AI](https://docs.crawl4ai.com/) with [OpenRouter](https://openrouter.ai/) to access the free Meta Llama 3.3 70B Instruct model for web crawling and content extraction.

## 🚀 Features

- **Free LLM Access**: Uses OpenRouter's free tier with Meta Llama 3.3 70B Instruct model
- **AI-Powered Crawling**: Leverages LLM for intelligent content extraction and processing
- **Multiple Strategies**: Simple crawling, LLM-based extraction, and comprehensive processing
- **Multiple Output Formats**: Markdown, JSON, HTML, and Raw data
- **Universal Configuration**: Single variable to control output format for all tasks
- **Batch Processing**: Efficient scraping of multiple websites
- **Error Handling**: Robust error handling and fallback mechanisms
- **Async Support**: High-performance asynchronous crawling

## 📋 Prerequisites

- Python 3.8+
- OpenRouter API key (free tier available)
- Internet connection

## 🛠️ Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your OpenRouter API key**:
   - Visit [OpenRouter](https://openrouter.ai/)
   - Sign up for a free account
   - Generate an API key from your dashboard
   - The free tier includes access to Meta Llama 3.3 70B Instruct

4. **Configure your API key**:
   - Edit `config.env` file
   - Replace `your_openrouter_api_key_here` with your actual API key

## 🎯 Quick Start

### Basic Usage

Run the comprehensive scraper:

```bash
python comprehensive_website_scraper.py
```

This will:
- Demonstrate single website scraping with multiple output formats
- Show batch scraping capabilities
- Generate markdown, JSON, and HTML outputs
- Display progress and results

### Usage Examples

For detailed usage examples:

```bash
python usage_example.py
```

This demonstrates:
- Single website scraping with different strategies
- Batch processing of multiple websites
- Custom extraction prompts
- Different output format combinations

### 🎛️ Universal Output Format Configuration

Easily configure output formats for all tasks by changing one variable in `usage_example.py`:

```python
# Options: "json", "markdown", "both", "all"
OUTPUT_FORMAT = "json"  # Change this to control all tasks
```

**Available Options:**
- `"json"`: Only JSON output
- `"markdown"`: Only markdown output
- `"both"`: Both JSON and markdown
- `"all"`: All formats (JSON, markdown, HTML, raw)

### 🚀 All-in-One Comprehensive Scraper

The main scraper provides:
- **Multiple Output Formats**: Markdown, JSON, HTML, and Raw data
- **Multiple Strategies**: Simple, LLM-based, and Comprehensive
- **Batch Processing**: Scrape multiple websites efficiently
- **Custom Prompts**: Define your own extraction prompts
- **Progress Tracking**: Real-time progress and summary reports
- **Error Handling**: Robust error handling and fallback mechanisms

## 📁 Project Structure

```
Crawl4Ai/
├── requirements.txt              # Python dependencies
├── config.env                    # Environment configuration
├── README.md                     # This file
├── comprehensive_website_scraper.py  # 🚀 All-in-one comprehensive scraper
├── usage_example.py              # 📖 Usage examples with universal config
├── test_basic.py                 # 🧪 Basic functionality tests
├── INSTALLATION.md               # 📋 Installation and troubleshooting guide
└── scraped_data/                 # 📁 Generated output files
    ├── *.md                      # Markdown outputs
    ├── *.json                    # JSON outputs
    └── scraping_summary_*.json   # Batch processing summaries
```

## 🔧 Configuration

### OpenRouter Settings

The `config.env` file contains:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
DEFAULT_MODEL=meta-llama/llama-3.3-70b-instruct:free
```

### Universal Output Format Configuration

Control all output formats with a single variable in `usage_example.py`:

```python
# Global configuration - Change this URL to test different websites
TARGET_URL = "https://example.com"

# Universal output format configuration
OUTPUT_FORMAT = "json"  # Options: "json", "markdown", "both", "all"
```

### LLM Configuration

The LLM is configured with these default settings:

```python
llm_config = {
    "provider": "openai",
    "api_key": api_key,
    "base_url": "https://openrouter.ai/api/v1",
    "model": "meta-llama/llama-3.3-70b-instruct:free",
    "temperature": 0.1,
    "max_tokens": 4000,
    "headers": {
        "HTTP-Referer": "https://github.com/crawl4ai-integration",
        "X-Title": "Comprehensive Website Scraper"
    }
}
```

## 🧠 LLM Integration Features

### 1. Simple Crawling
Basic web crawling without LLM (fastest):

```python
result = await scraper.scrape_website(
    url="https://example.com",
    strategy="simple",
    output_formats=["markdown", "json"]
)
```

### 2. LLM-Based Extraction
Extract specific information using custom prompts:

```python
result = await scraper.scrape_website(
    url="https://example.com",
    strategy="llm",
    output_formats=["json"],
    custom_prompt="Extract the main features and pricing information..."
)
```

### 3. Comprehensive Processing
Intelligent content processing with LLM extraction:

```python
result = await scraper.scrape_website(
    url="https://example.com",
    strategy="comprehensive",
    output_formats=["markdown", "json", "html"]
)
```

### 4. Batch Processing
Scrape multiple websites efficiently:

```python
results = await scraper.scrape_multiple_websites(
    urls=["https://site1.com", "https://site2.com"],
    strategy="comprehensive",
    output_formats=["markdown", "json"],
    delay=2
)
```

## 📊 Output Formats

### Markdown Output
Clean, structured markdown perfect for:
- RAG (Retrieval-Augmented Generation) pipelines
- Documentation generation
- Content analysis
- AI model training data

### Extracted Content
Structured data extracted using LLM prompts:
- JSON-formatted information
- Key-value pairs
- Categorized content

### Chunks
Intelligently segmented content for:
- Vector database storage
- Semantic search
- Batch processing

### 📊 Output Formats
Multiple output formats for different use cases:

**Markdown**: Clean, structured markdown perfect for RAG pipelines
**JSON**: Structured data with comprehensive extraction including:
- **Metadata**: URL, title, description, language, word count
- **Content**: Main headings, sub-headings, key points, call-to-actions
- **Navigation**: Menu items, breadcrumbs, footer links
- **Media**: Images, videos, documents
- **Business Info**: Company name, contact info, social media, pricing
- **Technical**: Technologies, forms, external links
- **Scraping Metadata**: Timestamp, model used, processing details
**HTML**: Raw HTML content for advanced processing
**Raw**: Complete raw data for custom analysis

## 🔍 Supported Models

This setup uses the **Meta Llama 3.3 70B Instruct** model via OpenRouter, which:

- **Multilingual**: Supports English, German, French, Italian, Portuguese, Hindi, Spanish, and Thai
- **Free Tier**: Available on OpenRouter's free plan
- **High Performance**: 70B parameter model with excellent reasoning capabilities
- **Context Length**: 65,536 tokens context window

## 🚨 Important Notes

1. **API Key Security**: Never commit your API key to version control
2. **Rate Limits**: Be aware of OpenRouter's rate limits on the free tier
3. **Model Availability**: The free model may have usage restrictions
4. **Content Rights**: Respect website terms of service and robots.txt
5. **Playwright Installation**: Run `playwright install` after installing dependencies
6. **Error Handling**: The scraper includes robust error handling and fallback mechanisms

## 🧪 Testing

### Basic Functionality Test
Test the configuration and error handling without requiring Playwright:

```bash
python test_basic.py
```

### Installation Verification
Follow the complete installation guide:

```bash
# See INSTALLATION.md for detailed steps
playwright install
python usage_example.py
```

## 🤝 Contributing

Feel free to:
- Report issues
- Suggest improvements
- Add new examples
- Enhance documentation

## 📚 Resources

- [Crawl4AI Documentation](https://docs.crawl4ai.com/)
- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [Meta Llama 3.3 Model Card](https://openrouter.ai/meta-llama/llama-3.3-70b-instruct:free/api)
- [Playwright Installation Guide](https://playwright.dev/python/docs/intro)

## 🎯 Usage Examples

### Single Task Execution
```bash
# Run specific tasks
python usage_example.py simple
python usage_example.py llm
python usage_example.py comprehensive
python usage_example.py batch
python usage_example.py custom
```

### Output Format Control
```python
# In usage_example.py, change OUTPUT_FORMAT:
OUTPUT_FORMAT = "json"      # JSON only
OUTPUT_FORMAT = "markdown"  # Markdown only
OUTPUT_FORMAT = "both"      # Both formats
OUTPUT_FORMAT = "all"       # All formats
```

### Custom Configuration
```python
# Change target URL
TARGET_URL = "https://your-website.com"

# Change output directory
OUTPUT_DIR = "your_output_folder"
```

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Crawling! 🕷️🤖** 