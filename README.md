# RabTech Web Scraping Pipeline - Milestone 04

Automated ETL web scraper using Python, Requests & BeautifulSoup.

## Overview
Scraped 60 books from books.toscrape.com with production-ready practices.

## Features Implemented
- Rate limiting (1 sec delay between requests)
- Custom headers & retry logic (3 retries)
- Parses raw HTML to structured data
- Exports to CSV & JSON
- Generates summary report

## Files in Repo
- scraper.py - Main scraper script with ETL pipeline
- requirements.txt - Dependencies (requests, beautifulsoup4)
- output.csv - 60 books structured data
- output.json - Same data in JSON format
- report.txt - Analytics summary

## How to Run
pip install -r requirements.txt
python scraper.py

## Tech Stack
Python, Requests, BeautifulSoup4, CSV, JSON

## Author
Muneswari Chitteti - RabTech Internship Milestone 04
