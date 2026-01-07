import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting rich data
        data = {
            "status_code": response.status_code,
            "title": soup.title.string if soup.title else "",
            "meta_description": "",
            "h1": [h.get_text().strip() for h in soup.find_all('h1')],
            "h2": [h.get_text().strip() for h in soup.find_all('h2')],
            "links": [a.get('href') for a in soup.find_all('a', href=True)],
            "images": [{"alt": img.get('alt', ''), "src": img.get('src', '')} for img in soup.find_all('img')],
            "full_text": soup.get_text()
        }

        meta = soup.find("meta", attrs={'name': 'description'})
        if meta:
            data["meta_description"] = meta.get("content", "")

        return data
    except Exception as e:
        return {"error": str(e), "status_code": 500}