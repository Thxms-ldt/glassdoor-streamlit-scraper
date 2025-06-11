import streamlit as st
import pandas as pd
from scraper import scrap_glassdoor_reviews

st.set_page_config(page_title="Glassdoor Scraper", layout="centered")
st.title("🔍 Glassdoor Reviews Scraper (BeautifulSoup)")

st.markdown(
    """
    Cette application permet de récupérer les avis Glassdoor **publiques** d'une entreprise (pas besoin de compte).
    
    1. **Collez l'URL** de la page d'avis Glassdoor (ex: https://www.glassdoor.fr/Avis/WeFiiT-Avis-E3310403.htm)
    2. **Choisissez le nombre de pages à récupérer**
    3. Cliquez sur **Lancer le scraping** et téléchargez le CSV !
    """
)

# Saisie de l'URL
url = st.text_input(
    "URL de la page Glassdoor des avis :",
    value="https://www.glassdoor.fr/Avis/WeFiiT-Avis-E3310403.htm"
)

pages = st.number_input(
    "Nombre de pages à scraper :", min_value=1, max_value=20, value=3, step=1
)

if st.button("Lancer le scraping"):
    st.info("Scraping en cours... Cela peut prendre quelques secondes.")
    data = scrap_glassdoor_reviews(url, int(pages))
    if data and len(data) > 0:
        df = pd.DataFrame(data)
        st.success(f"{len(df)} avis récupérés ! Aperçu :")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Télécharger en CSV", csv, "avis_glassdoor.csv", "text/csv")
    else:
        st.error("❌ Aucune donnée récupérée. Vérifiez l'URL ou réessayez plus tard.")
else:
    st.write("Veuillez entrer l'URL d'une page d'avis Glassdoor et cliquer sur le bouton.")
