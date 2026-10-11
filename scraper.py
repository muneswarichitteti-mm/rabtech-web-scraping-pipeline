import requests
from bs4 import BeautifulSoup
import csv, json, time, random, statistics
from dataclasses import dataclass
from datetime import datetime
from collections import Counter

@dataclass
class Book:
    title: str
    price: float
    rating: str
    availability: str
    url: str

class WebScraperPipeline:
    BASE_URL = "http://books.toscrape.com/"
    HEADERS = {"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"}

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.books = []

    def fetch_with_retry(self, url, retries=3):
        for i in range(retries):
            try:
                print(f"Fetching: {url}")
                r = self.session.get(url, timeout=10)
                r.raise_for_status()
                return r
            except Exception as e:
                print(f"Retry {i+1}: {e}")
                time.sleep((2**i) + random.uniform(0,1))
        raise Exception("Failed")

    def parse_books(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        books = []
        for article in soup.select('article.product_pod'):
            title = article.h3.a['title']
            price = float(article.select_one('p.price_color').text.replace('£','').replace('Â',''))
            rating = article.select_one('p.star-rating')['class'][1]
            availability = article.select_one('p.instock').text.strip()
            url = article.h3.a['href']
            books.append(Book(title, price, rating, availability, url))
        return books

    def scrape(self, pages=3):
        print(f"\nSTARTING SCRAPING {pages} pages\n")
        for page in range(1, pages+1):
            if page>1: time.sleep(1)
            url = self.BASE_URL if page==1 else f"{self.BASE_URL}catalogue/page-{page}.html"
            resp = self.fetch_with_retry(url)
            self.books.extend(self.parse_books(resp.text))
            print(f"Page {page}: {len(self.books)} books")
        return self.books

    def save_csv(self):
        with open('output.csv','w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=['title','price','rating','availability','url'])
            w.writeheader()
            for b in self.books: w.writerow(b.__dict__)
        print("Saved output.csv")

    def save_json(self):
        with open('output.json','w',encoding='utf-8') as f:
            json.dump([b.__dict__ for b in self.books], f, indent=2)
        print("Saved output.json")

    def generate_report(self):
        prices=[b.price for b in self.books]
        report=f"""Report
Total: {len(self.books)}
Avg: {statistics.mean(prices):.2f}
Min: {min(prices)} Max: {max(prices)}
Ratings: {Counter([b.rating for b in self.books])}
Date: {datetime.now()}
Ethics: headers, rate limit, retry done
"""
        print(report)
        open('report.txt','w').write(report)

if __name__=="__main__":
    s=WebScraperPipeline()
    s.scrape(pages=3)
    s.save_csv()
    s.save_json()
    s.generate_report()