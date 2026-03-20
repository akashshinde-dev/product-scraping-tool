
# Advanced Multi-Page Web Scraper in Python

## Description

This project demonstrates a **robust Python web scraper** capable of collecting structured data from multiple pages of a website and saving it safely into CSV files.

It features **automatic pagination**, **random User-Agent rotation** to reduce blocking, **retry logic**, and **safe CSV writing**. The project highlights skills in **Python programming**, **web scraping**, and **data handling**.

---

## Key Features

* Scrapes data from multiple pages automatically
* Random User-Agent support to reduce request blocking
* Retry mechanism for failed requests
* Saves data safely and reliably into CSV files
* Handles missing or inconsistent data gracefully
* Modular and reusable code design

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### 2. Install dependencies

```bash
pip install requests beautifulsoup4 fake-useragent
```

---

## Usage

### Import modules

```python
from scraper import MultiPageScraper
from save_to_csv import csv_dict
```

### Create scraper and run

```python
scraper = MultiPageScraper()

data = scraper.scrape_multi_pages(
    "http://books.toscrape.com/",  # Replace with your target URL
    item_selector,
    fields,
    next_page_selector,
    stop_page=2
)

csv_dict.save(data, file_name="output.csv")
```

> **Note:** Define `item_selector`, `fields`, and `next_page_selector` according to the structure of the target website.

---

## How It Works

1. **Define selectors**: Specify which HTML elements to extract.
2. **Pagination support**: Automatically follows “next page” links until the last page or a defined page limit.
3. **Data collection**: Extracts all fields from each page.
4. **CSV export**: Saves the data safely into CSV files, avoiding overwrites unless specified.

---

## Skills Demonstrated

* Python 3.x programming and object-oriented design
* Web scraping with **Requests** and **BeautifulSoup**
* Randomized User-Agent handling to mimic human browsing
* Error handling and retry logic for robust scripts
* Data validation and CSV export

---

## Example Output

```csv
Book_name,Price,Rating,Stock,Book_url
"A Light in the Attic","£51.77","Three","In stock","http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
"Tipping the Velvet","£53.74","One","In stock","http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
```

---

## Notes

* Best used on websites that **allow scraping**
* Always scrape responsibly; avoid sending too many requests in a short time
* Modular code allows easy adaptation to different websites
