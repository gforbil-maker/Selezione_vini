import os
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def save_debug_html(shop_name, html):
    os.makedirs("debug_html", exist_ok=True)
    with open(f"debug_html/{shop_name}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"💾 Salvato debug_html/{shop_name}.html ({len(html)} caratteri)")


def get_html_with_playwright(url):
    html_content = ""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                viewport={'width': 1366, 'height': 768}
            )
            page = context.new_page()
            print(f"Navigazione verso: {url}")
            page.goto(url, timeout=40000, wait_until="networkidle")
            time.sleep(3)
            html_content = page.content()
            browser.close()
    except Exception as e:
        print(f"❌ Errore durante il caricamento di {url}: {e}")
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
        cards = soup.select('.product-item') or soup.select('[data-product-id]') or soup.select('.card')
        print(f"🔎 Tannico: trovate {len(cards)} schede prodotto.")

        if len(cards) == 0:
            save_debug_html("tannico", html)

        for card in cards:
            title_el = card.select_one('.product-item-name, .product-name, a.product-item-link, .title, h3, h2')
            price_el = card.select_one('.price, .special-price, .price-final_price, .final-price')
            link_el = card.select_one('a')

            if title_el and price_el:
                title = title_el.get_text(strip=True)
                price = price_el.get_text(strip=True)
                raw_link = link_el['href'] if link_el and 'href' in link_el.attrs else "/sconti.html"
                wines.append({
                    'title': title,
                    'price': price,
                    'link': fix_link(raw_link, base_url)
                })
                if len(wines) >= 4:
                    break
    else:
        print("⚠️ Tannico: HTML vuoto (probabile errore di caricamento pagina).")
    return wines


def scrape_vinatis():
    wines = []
    base_url = "https://www.vinatis.it"
    html = get_html_with_playwright(f"{base_url}/promozioni")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.product-block, .product-card, .product-item, .product-container, [data-id-product]')
        print(f"🔎 Vinatis: trovate {len(cards)} schede prodotto.")

        if len(cards) == 0:
            save_debug_html("vinatis", html)

        for card in cards:
            title_el = card.select_one('.product-name, .name, .title, h3, h2')
            price_el = card.select_one('.price, .promo-price, .special-price, .our-price')
            link_el = card.select_one('a')

            if title_el and price_el:
                title = title_el.get_text(strip=True)
                price = price_el.get_text(strip=True)
                raw_link = link_el['href'] if link_el and 'href' in link_el.attrs else "/promozioni"
                wines.append({
                    'title': title,
                    'price': price,
                    'link': fix_link(raw_link, base_url)
                })
                if len(wines) >= 4:
                    break
    else:
        print("⚠️ Vinatis: HTML vuoto (probabile errore di caricamento pagina).")
    return wines


def scrape_callmewine():
    wines = []
    base_url = "https://www.callmewine.com"
    html = get_html_with_playwright(f"{base_url}/promozioni.html")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.product-item, .card-product, .product-card, .item')
        print(f"🔎 Callmewine: trovate {len(cards)} schede prodotto.")

        if len(cards) == 0:
            save_debug_html("callmewine", html)

        for card in cards:
            title_el = card.select_one('.product-item-link, .product-name, .name, h3, h2')
            price_el = card.select_one('.price, .special-price, .final-price')
            link_el = card.select_one('a')

            if title_el and price_el:
                title = title_el.get_text(strip=True)
                price = price_el.get_text(strip=True)
                raw_link = link_el['href'] if link_el and 'href' in link_el.attrs else "/promozioni.html"
                wines.append({
                    'title': title,
                    'price': price,
                    'link': fix_link(raw_link, base_url)
                })
                if len(wines) >= 4:
                    break
    else:
        print("⚠️ Callmewine: HTML vuoto (probabile errore di caricamento pagina).")
    return wines


def get_wine_deals():
    deals = {
        'Tannico': scrape_tannico(),
        'Vinatis': scrape_vinatis(),
        'Callmewine': scrape_callmewine()
    }

    if not deals['Tannico']:
        print("⚠️ Tannico vuoto: attivo fallback")
        deals['Tannico'] = [
            {'title': 'Pinot Nero Alto Adige DOC', 'price': '16,90 €', 'link': 'https://www.tannico.it/sconti.html'},
            {'title': 'Chianti Classico Riserva', 'price': '14,50 €', 'link': 'https://www.tannico.it/sconti.html'}
        ]
    if not deals['Vinatis']:
        print("⚠️ Vinatis vuoto: attivo fallback")
        deals['Vinatis'] = [
            {'title': 'Bordeaux Supérieur 2020', 'price': '11,80 €', 'link': 'https://www.vinatis.it/promozioni'}
        ]
    if not deals['Callmewine']:
        print("⚠️ Callmewine vuoto: attivo fallback")
        deals['Callmewine'] = [
            {'title': 'Nebbiolo d\'Alba 2021', 'price': '15,20 €', 'link': 'https://www.callmewine.com/promozioni.html'}
        ]

    return deals


if __name__ == "__main__":
    data = get_wine_deals()
    print("Fine estrazione:", data)
