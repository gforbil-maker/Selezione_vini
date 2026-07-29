# name: Aggiorna Selezione Vini

on:
  schedule:
    - cron: '0 7 * * *'  # Esegue ogni giorno alle 07:00 UTC
  workflow_dispatch:      # Permette l'esecuzione manuale

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout codice
        uses: actions/checkout@v3

      - name: Configura Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Installa dipendenze e Playwright
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4 playwright
          playwright install chromium

      - name: Esegui scraper
        run: python build_site.py || python scraper.py

      - name: Commit e Push dei cambiamenti
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add index.html
          git commit -m "Aggiornamento automatico vini del giorno" || exit 0
          git push
Deprecated: renamed to 
