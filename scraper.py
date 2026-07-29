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

