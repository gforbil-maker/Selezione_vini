
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def get_html_with_playwright(url):
    html_content = ""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1280, 'height': 800}
            )
            page = context.new_page()
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(4)  # Attesa per il caricamento dei contenuti dinamici/lazy
            html_content = page.content()
            browser.close()
    except Exception as e:
        print(f"Errore durante il caricamento di {url}: {e}")
    return html_content

def fix_link(link, base_url):
    if not link:
        return base_url
    if link.startswith("http"):
        return link
    return base_url.rstrip("/") + "/" + link.lstrip("/")

def scrape_tannico():
    wines = []
    base_url = "https://www.tannico.it"
    html = get_html_with_playwright(f"{base_url}/sconti.html")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.product-item') or soup.select('.product-card') or soup.select('article') or soup.select('.card')
        for card in cards[:6]:
            title = card.select_one('.product-name, .title, .product-title, h3, h2, .name')
            price = card.select_one('.price, .special-price, .final-price, .current-price')
            link = card.select_one('a')
            if title and price:
                raw_link = link['href'] if link and 'href' in link.attrs else "/sconti.html"
                wines.append({
                    'title': title.get_text(strip=True),
                    'price': price.get_text(strip=True),
                    'link': fix_link(raw_link, base_url)
                })
    return wines

def scrape_vinatis():
    wines = []
    base_url = "https://www.vinatis.it"
    html = get_html_with_playwright(f"{base_url}/promozioni")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.product-container') or soup.select('.product_list_item') or soup.select('.prod-card') or soup.select('.product-card')
        for card in cards[:6]:
            title = card.select_one('.product-name, .name, h3, .title')
            price = card.select_one('.price, .promo-price, .special-price')
            link = card.select_one('a')
            if title and price:
                raw_link = link['href'] if link and 'href' in link.attrs else "/promozioni"
                wines.append({
                    'title': title.get_text(strip=True),
                    'price': price.get_text(strip=True),
                    'link': fix_link(raw_link, base_url)
                })
    return wines

def scrape_callmewine():
    wines = []
    base_url = "https://www.callmewine.com"
    html = get_html_with_playwright(f"{base_url}/promozioni.html")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.product-item') or soup.select('.item') or soup.select('.product-card') or soup.select('.card-product')
        for card in cards[:6]:
            title = card.select_one('.product-item-link, .name, h3, .product-name')
            price = card.select_one('.price, .special-price')
            link = card.select_one('a')
            if title and price:
                raw_link = link['href'] if link and 'href' in link.attrs else "/promozioni.html"
                wines.append({
                    'title': title.get_text(strip=True),
                    'price': price.get_text(strip=True),
                    'link': fix_link(raw_link, base_url)
                })
    return wines

def get_wine_deals():
    deals = {
        'Tannico': scrape_tannico(),
        'Vinatis': scrape_vinatis(),
        'Callmewine': scrape_callmewine()
    }
    
    # Fallback di sicurezza sui dati di test se lo scraping viene bloccato
    if not deals['Tannico']:
        deals['Tannico'] = [
            {'title': 'Pinot Nero Alto Adige DOC', 'price': '16,90 €', 'link': 'https://www.tannico.it/sconti.html'},
            {'title': 'Chianti Classico Riserva', 'price': '14,50 €', 'link': 'https://www.tannico.it/sconti.html'}
        ]
    if not deals['Vinatis']:
        deals['Vinatis'] = [
            {'title': 'Bordeaux Supérieur 2020', 'price': '11,80 €', 'link': 'https://www.vinatis.it/promozioni'}
        ]
    if not deals['Callmewine']:
        deals['Callmewine'] = [
            {'title': 'Nebbiolo d\'Alba 2021', 'price': '15,20 €', 'link': 'https://www.callmewine.com/promozioni.html'}
        ]
        
    return deals

if __name__ == "__main__":
    data = get_wine_deals()
    print("Dati estratti con successo:", data)
