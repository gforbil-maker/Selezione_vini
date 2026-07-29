import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def get_html_with_playwright(url):
    html_content = ""
    try:
        with sync_playwright() as p:
            # Avvia un browser Chromium in modalità headless
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            # Imposta timeout di 30 secondi
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(3)  # Attesa per il rendering dinamico dei contenuti
            html_content = page.content()
            browser.close()
    except Exception as e:
        print(f"Errore durante il caricamento di {url}: {e}")
    return html_content

def scrape_tannico():
    wines = []
    html = get_html_with_playwright("https://www.tannico.it/sconti.html")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.product-item') or soup.select('.product-card') or soup.select('article')
        for card in cards[:6]:
            title = card.select_one('.product-name, .title, .product-title, h3, h2')
            price = card.select_one('.price, .special-price, .final-price')
            link = card.select_one('a')
            if title and price:
                wines.append({
                    'title': title.get_text(strip=True),
                    'price': price.get_text(strip=True),
                    'link': link['href'] if link and 'href' in link.attrs else "https://www.tannico.it"
                })
    return wines

def scrape_vinatis():
    wines = []
    html = get_html_with_playwright("https://www.vinatis.it/promozioni")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.product-container') or soup.select('.product_list_item') or soup.select('.prod-card')
        for card in cards[:6]:
            title = card.select_one('.product-name, .name, h3')
            price = card.select_one('.price, .promo-price')
            link = card.select_one('a')
            if title and price:
                wines.append({
                    'title': title.get_text(strip=True),
                    'price': price.get_text(strip=True),
                    'link': link['href'] if link and 'href' in link.attrs else "https://www.vinatis.it"
                })
    return wines

def scrape_callmewine():
    wines = []
    html = get_html_with_playwright("https://www.callmewine.com/promozioni.html")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.product-item') or soup.select('.item') or soup.select('.product-card')
        for card in cards[:6]:
            title = card.select_one('.product-item-link, .name, h3')
            price = card.select_one('.price')
            link = card.select_one('a')
            if title and price:
                wines.append({
                    'title': title.get_text(strip=True),
                    'price': price.get_text(strip=True),
                    'link': link['href'] if link and 'href' in link.attrs else "https://www.callmewine.com"
                })
    return wines

def get_wine_deals():
    return {
        'Tannico': scrape_tannico(),
        'Vinatis': scrape_vinatis(),
        'Callmewine': scrape_callmewine()
    }

if __name__ == "__main__":
    data = get_wine_deals()
    print("Dati estratti:", data)
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7'
}

def scrape_tannico():
    wines = []
    try:
        url = "https://www.tannico.it/sconti.html"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Cerca i prodotti all'interno della griglia promozioni
            cards = soup.select('.product-item') or soup.select('.product-card')
            for card in cards[:6]:
                title = card.select_one('.product-name, .title, .product-title')
                price = card.select_one('.price, .special-price, .final-price')
                link = card.select_one('a')
                if title and price:
                    wines.append({
                        'title': title.get_text(strip=True),
                        'price': price.get_text(strip=True),
                        'link': link['href'] if link and 'href' in link.attrs else url
                    })
    except Exception as e:
        print(f"Errore Tannico: {e}")
    return wines

def scrape_vinatis():
    wines = []
    try:
        url = "https://www.vinatis.it/promozioni"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            cards = soup.select('.product-container') or soup.select('.product_list_item')
            for card in cards[:6]:
                title = card.select_one('.product-name, .name')
                price = card.select_one('.price')
                link = card.select_one('a')
                if title and price:
                    wines.append({
                        'title': title.get_text(strip=True),
                        'price': price.get_text(strip=True),
                        'link': link['href'] if link and 'href' in link.attrs else url
                    })
    except Exception as e:
        print(f"Errore Vinatis: {e}")
    return wines

def scrape_callmewine():
    wines = []
    try:
        url = "https://www.callmewine.com/promozioni.html"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            cards = soup.select('.product-item') or soup.select('.item')
            for card in cards[:6]:
                title = card.select_one('.product-item-link, .name')
                price = card.select_one('.price')
                link = card.select_one('a')
                if title and price:
                    wines.append({
                        'title': title.get_text(strip=True),
                        'price': price.get_text(strip=True),
                        'link': link['href'] if link and 'href' in link.attrs else url
                    })
    except Exception as e:
        print(f"Errore Callmewine: {e}")
    return wines

def get_wine_deals():
    return {
        'Tannico': scrape_tannico(),
        'Vinatis': scrape_vinatis(),
        'Callmewine': scrape_callmewine()
    }

if __name__ == "__main__":
    data = get_wine_deals()
    print("Dati estratti con successo:", data)

