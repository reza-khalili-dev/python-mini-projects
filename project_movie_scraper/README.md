# Project 10 — Movie & TV Scraper (IMDB)

A desktop GUI app to search movies and TV shows on IMDb using Selenium, then present results with poster, title, year, genres and IMDb rating.  
Features planned:
- Search by title, genre, year, min-rating
- Show results as a grid with poster + title + genre + year
- Click a result to open its IMDb page in the browser
- Filters: minimum rating, specific year, genre dropdown
- Built with Python, Selenium, webdriver-manager and ttkbootstrap

## Quick start (dev)

1. Install Python 3.10+  
2. Install dependencies:
```bash
pip install -r requirements.txt

python main.py

Notes

This project uses Selenium to scrape IMDb pages. Make sure Google Chrome (or Chromium) is installed on your machine. webdriver-manager will download the correct driver automatically.

We will keep the UI responsive by running scraping in background threads.

