import requests
from bs4 import BeautifulSoup

def scrap_glassdoor_reviews(url, pages=1):
    reviews = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    for page in range(1, pages + 1):
        # Construction de l'URL de la page suivante
        if page == 1:
            page_url = url
        else:
            # Si l'URL contient déjà '?', gérer les paramètres
            if "?" in url:
                page_url = url.split("?")[0] + f"_P{page}.htm?" + url.split("?")[1]
            else:
                page_url = url.replace('.htm', f'_P{page}.htm')

        print(f"==== [Scraping] URL: {page_url}")
        response = requests.get(page_url, headers=headers)
        print("========= DEBUT HTML =========")
        print(response.text[:1000])   # On log uniquement le début
        print("========== FIN HTML ==========")

        if response.status_code != 200:
            print(f"Erreur de chargement de la page {page_url} (code {response.status_code})")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        review_blocks = soup.find_all("div", {"data-test": "review-details-container"})
        print(f"Trouvé {len(review_blocks)} avis sur la page {page}")

        for block in review_blocks:
            titre = block.find("span", {"lang": True})
            titre = titre.text.strip() if titre else ""
            note = block.find("span", {"data-test": "review-rating-label"})
            note = note.text.strip() if note else ""
            date = block.find("span", class_="timestamp_reviewDate__dsF9n")
            date = date.text.strip() if date else ""
            avantages = block.find("span", {"data-test": "review-text-PROS"})
            avantages = avantages.text.strip() if avantages else ""
            inconvenients = block.find("span", {"data-test": "review-text-CONS"})
            inconvenients = inconvenients.text.strip() if inconvenients else ""

            reviews.append({
                "titre": titre,
                "note": note,
                "date": date,
                "avantages": avantages,
                "inconvenients": inconvenients,
            })

    return reviews
