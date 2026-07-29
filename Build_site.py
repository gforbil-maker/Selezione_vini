import scraper

# Recupera i dati dal file scraper.py
deals = scraper.get_wine_deals()

# Crea il codice HTML con i vini estratti
html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Selezione Vini del Giorno</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f9f8f6; color: #333; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: auto; }}
        h1 {{ text-align: center; color: #722F37; }}
        .subtitle {{ text-align: center; color: #666; margin-bottom: 30px; }}
        .card {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .shop-title {{ color: #722F37; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 0; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ padding: 10px 0; border-bottom: 1px solid #f1f1f1; display: flex; justify-content: space-between; align-items: center; }}
        li:last-child {{ border-bottom: none; }}
        .wine-info {{ max-width: 70%; }}
        .wine-title {{ font-weight: bold; color: #333; display: block; }}
        .wine-price {{ color: #b22222; font-weight: bold; font-size: 1.1em; }}
        .btn {{ background-color: #722F37; color: white; padding: 8px 12px; text-decoration: none; border-radius: 5px; font-size: 0.9em; }}
        .btn:hover {{ background-color: #5a232b; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🍷 Selezione Vini del Giorno</h1>
        <div class="subtitle">Aggiornato automaticamente ogni giorno da Tannico, Vinatis e Callmewine</div>
"""

# Aggiunge le sezioni per ogni negozio
for shop, wines in deals.items():
    html_content += f"""
        <div class="card">
            <h2 class="shop-title">{shop}</h2>
            <ul>
    """
    if wines:
        for wine in wines:
            html_content += f"""
                <li>
                    <div class="wine-info">
                        <span class="wine-title">{wine.get('title')}</span>
                        <span class="wine-price">{wine.get('price')}</span>
                    </div>
                    <a href="{wine.get('link')}" class="btn" target="_blank">Vedi offerta</a>
                </li>
            """
    else:
        html_content += "<li><p>Nessuna offerta trovata al momento.</p></li>"
        
    html_content += """
            </ul>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

# Salva tutto nel file index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Pagina index.html generata con successo!")
