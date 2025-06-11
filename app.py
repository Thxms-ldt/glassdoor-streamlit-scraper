import streamlit as st
import pandas as pd
from scraper import scrap_glassdoor_reviews

st.title("🔍 Glassdoor Reviews Scraper (BeautifulSoup only)")
st.markdown("**Scrapez facilement tous les avis d’une société Glassdoor (ex : WeFiiT) sans login ni Selenium.**")

url = st.text_input(
    "Collez l’URL de la page Glassdoor des avis à scraper :",
    value="https://www.glassdoor.fr/Avis/WeFiiT-Avis-E3310403.htm"
)

nb_pages = st.number_input("Nombre de pages à scraper :", min_value=1, max_value=15, value=7)

if st.button("Lancer le scraping"):
    with st.spinner("Scraping en cours..."):
        avis = scrap_glassdoor_reviews(url, nb_pages)
    if avis:
        df = pd.DataFrame(avis)
        st.success(f"{len(df)} avis récupérés ✅")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Télécharger CSV", csv, "avis_glassdoor.csv")
    else:
        st.error("❌ Aucune donnée récupérée. Essayez une autre URL ou attendez un peu (Glassdoor limite parfois).")

st.markdown("---")
st.info("Aucune authentification n'est nécessaire tant que les avis sont accessibles sans login Glassdoor.")
