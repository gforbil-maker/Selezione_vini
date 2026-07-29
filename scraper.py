import urllib.request
from bs4 import BeautifulSoup
import json
import os

def fetch_html(url):
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Errore caricando {url}: {e}")
        return ""

def scrape_vini():
    offerte = {
        "tannico": [],
        "vinatis": [],
        "callmewine": []
    }

    # 1. Tannico - Promozioni
    html = fetch_html("https://www.tannico.it/promozioni.html")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.find_all('div', class_='product-item', limit=3)
        for p in products:
            title = p.find('a', class_='product-item-link')
            price = p.find('span', class_='price')
            link = title['href'] if title else 'https://www.tannico.it'
            name = title.text.strip() if title else 'Vino in promozione'
            cost = price.text.strip() if price else 'Vedi sito'
            offerte["tannico"].append({"nome": name, "prezzo": cost, "link": link})

    # 2. Vinatis - Promozioni
    html = fetch_html("https://www.vinatis.it/promozioni")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.find_all('div', class_='product_card', limit=3)
        for p in products:
            title = p.find('a', class_='product_name')
            price = p.find('span', class_='price')
            link = title['href'] if title else 'https://www.vinatis.it'
            name = title.text.strip() if title else 'Vino in promozione'
            cost = price.text.strip() if price else 'Vedi sito'
            offerte["vinatis"].append({"nome": name, "prezzo": cost, "link": link})

    # 3. Callmewine - Sconti
    html = fetch_html("https://www.callmewine.com/sconti-e-promozioni-C83.htm")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.find_all('div', class_='product-item', limit=3)
        for p in products:
            title = p.find('a', class_='product-item-link')
            price = p.find('span', class_='price')
            link = title['href'] if title else 'https://www.callmewine.com'
            name = title.text.strip() if title else 'Vino in promozione'
            cost = price.text.strip() if price else 'Vedi sito'
            offerte["callmewine"].append({"nome": name, "prezzo": cost, "link": link})

    # Genera pagina HTML
    html_out = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Selezione Vini del Giorno</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background-color: #f8f6f0; color: #2c2c2c; padding: 20px; max-width: 800px; margin: 0 auto; }}
        h1 {{ text-align: center; color: #722f37; font-size: 1.8rem; margin-bottom: 5px; }}
        .subtitle {{ text-align: center; font-size: 0.9rem; color: #666; margin-bottom: 25px; }}
        .section {{ background: white; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        .section h2 {{ color: #722f37; border-bottom: 2px solid #f0e6df; padding-bottom: 8px; margin-top: 0; font-size: 1.3rem; }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ padding: 12px 0; border-bottom: 1px solid #f5f5f5; display: flex; justify-content: space-between; align-items: center; gap: 10px; }}
        li:last-child {{ border-bottom: none; }}
        a {{ color: #1a0dab; text-decoration: none; font-weight: 600; flex: 1; }}
        a:hover {{ text-decoration: underline; }}
        .price {{ background: #e6f4ea; color: #137333; font-weight: bold; padding: 4px 10px; border-radius: 20px; font-size: 0.9rem; white-space: nowrap; }}
    </style>
</head>
<body>
    <h1>🍷 Selezione Vini del Giorno</h1>
    <p class="subtitle">Aggiornato automaticamente ogni giorno da Tannico, Vinatis e Callmewine</p>
"""
    
    nomi_siti = {"tannico": "Tannico", "vinatis": "Vinatis", "callmewine": "Callmewine"}
    
    for key, items in offerte.items():
        html_out += f'<div class="section"><h2>{nomi_siti[key]}</h2><ul>'
        if items:
            for item in items:
                html_out += f'<li><a href="{item["link"]}" target="_blank">{item["nome"]}</a><span class="price">{item["prezzo"]}</span></li>'
        else:
            html_out += f'<li><a href="https://www.{key}.it" target="_blank">Visita la sezione promozioni</a><span class="price">Vedi sito</span></li>'
        html_out += '</ul></div>'

    html_out += """
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_out)

if __name__ == "__main__":
    scrape_vini()
