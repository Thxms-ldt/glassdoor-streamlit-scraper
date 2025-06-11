import requests
from bs4 import BeautifulSoup

def scrap_glassdoor_reviews(url, nb_pages=7):
    avis_total = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/137.0.0.0 Safari/537.36"
    }

    for page in range(1, nb_pages + 1):
        if page == 1:
            page_url = url
        else:
            page_url = url.replace('.htm', f'_P{page}.htm?filter.iso3Language=fra')
        print(f"Scraping page: {page_url}")

        response = requests.get(page_url, headers=headers)
        if response.status_code != 200:
            print(f"Erreur de chargement de la page {page_url} (code {response.status_code})")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        avis_divs = soup.find_all("div", {"data-test": "review-details-container"})

        for avis in avis_divs:
            try:
                note = avis.select_one("[data-test='review-rating-label']")
                note = note.get_text(strip=True) if note else ""
                titre = avis.select_one("[data-test='review-details-title']")
                titre = titre.get_text(strip=True) if titre else ""
                date = avis.select_one(".timestamp_reviewDate__dsF9n")
                date = date.get_text(strip=True) if date else ""
                poste = avis.select_one(".review-avatar_avatarLabel__P15ey")
                poste = poste.get_text(strip=True) if poste else ""
                ville = ""
                ville_span = avis.select_one(".text-with-icon_LabelContainer__xbtB8")
                if ville_span:
                    ville = ville_span.get_text(strip=True)
                else:
                    ville = ""
                avantages = avis.select_one("span[data-test='review-text-PROS']")
                avantages = avantages.get_text(strip=True) if avantages else ""
                inconvenients = avis.select_one("span[data-test='review-text-CONS']")
                inconvenients = inconvenients.get_text(strip=True) if inconvenients else ""

                avis_total.append({
                    "note": note,
                    "titre": titre,
                    "date": date,
                    "poste": poste,
                    "ville": ville,
                    "avantages": avantages,
                    "inconvenients": inconvenients,
                })
            except Exception as e:
                print("Erreur sur un avis :", e)
    return avis_total
