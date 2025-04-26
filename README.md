# Part Picker AI

An intelligent automotive parts search system that helps users find specific car parts in junkyards using natural language processing and real-time inventory search.

## Overview

This project provides an intuitive interface for searching automotive parts across junkyard inventories. It uses AI to interpret natural language queries, standardize vehicle information, and find the most relevant matches based on multiple criteria including model year, color, and yard date.

## Features

- Natural language query processing for car parts
- Intelligent parsing of make, model, year, and part information
- Real-time junkyard inventory searching
- Smart ranking system for matching vehicles considering:
  - Model year proximity (±5 years)
  - Color matching
  - Recent yard arrivals
- Match scoring system (0-100%)
- Standardized vehicle naming (e.g., "Miata" → "MX-5 MIATA")

## Tech Stack

- **Python 3.10+**
- **OpenAI GPT-4** - For natural language processing and query interpretation
- **Libraries:**
  - `openai` - OpenAI API integration
  - `requests` - HTTP requests for inventory searching
  - `beautifulsoup4` - Web scraping and HTML parsing
  - `python-dotenv` - Environment variable management
  - `urllib` - URL encoding

## Setup

1. Clone the repository
2. Install requirements:
   ```
   pip install openai requests beautifulsoup4 python-dotenv
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```
   python main.py
   ```

## Usage

Simply run the program and enter your query when prompted. Example queries:
- "2010 honda civic black door"
- "alternator for a 1990 mazda miata"
- "2015 toyota camry transmission"

The system will interpret your query, search available inventory, and return the top 3 matching vehicles with match scores. Example response:

🏆 Top 3 Recommended Cars:
1. 2009 Honda Civic (Black) - Yard Date: 04/11/2025 - Match Score: 90%
2. 2006 Honda Civic (Black) - Yard Date: 04/24/2025 - Match Score: 85%
3. 2012 Honda Civic (Black) - Yard Date: 03/25/2025 - Match Score: 80%
