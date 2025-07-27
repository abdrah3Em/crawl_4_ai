# Installation Guide

## Prerequisites

1. **Python 3.8+** installed
2. **OpenRouter API Key** (free tier available)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Install Playwright Browsers

The main error you're seeing is because Playwright browsers are not installed. Run this command:

```bash
playwright install
```

This will install the required browsers for web scraping.

## Step 3: Configure API Key

Edit the `config.env` file and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
DEFAULT_MODEL=meta-llama/llama-3.3-70b-instruct:free
```

## Step 4: Test Installation

Run the basic test to verify everything is working:

```bash
python test_basic.py
```

## Step 5: Run the Scraper

Now you can run the main scraper:

```bash
# Run all tasks
python usage_example.py

# Run specific task
python usage_example.py simple
python usage_example.py llm
python usage_example.py comprehensive
```

## Troubleshooting

### Playwright Installation Issues

If you get Playwright errors, try:

```bash
# Install Playwright browsers
playwright install

# Or install specific browser
playwright install chromium

# If still having issues, try reinstalling
pip uninstall playwright
pip install playwright
playwright install
```

### API Key Issues

Make sure your `config.env` file contains a valid OpenRouter API key.

### Permission Issues

On Windows, you might need to run as administrator or check Windows Defender settings.

## Alternative: Test Without Playwright

If you want to test the basic functionality without installing Playwright browsers, run:

```bash
python test_basic.py
```

This will test the configuration and error handling without requiring browser installation. 