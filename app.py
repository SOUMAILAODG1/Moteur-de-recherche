import streamlit as st
import wikipediaapi
import requests
from bs4 import BeautifulSoup

# Configuration de l'application Streamlit
st.set_page_config(page_title="Moteur de Recherche Multisource", layout="wide")

# Titre de l'application
st.title("🔍 Moteur de Recherche Multisource")

# Sidebar pour les paramètres
with st.sidebar:
    st.header("Paramètres")
    language = st.selectbox("Langue Wikipédia", ["fr", "en", "es", "de"], index=0)
    max_results = st.slider("Nombre max de résultats externes", 1, 10, 5)

# Zone de recherche
search_term = st.text_input("Entrez un terme de recherche:", "")

# Initialisation de l'API Wikipédia
wiki = wikipediaapi.Wikipedia(
    language=language,
    user_agent='MonMoteurRechercheRI/1.0 (contact@example.com)'
)

def display_wiki_info(page):
    """Affiche les informations Wikipédia"""
    if page.exists():
        with st.expander(f"📖 {page.title} (Wikipédia)", expanded=True):
            st.write(f"**Résumé:** {page.summary[:500]}...")
            st.write(f"**URL:** {page.fullurl}")
            st.markdown(f"**Langue:** `{page.language}`")
            st.markdown(f"**Nombre de mots:** `{page.text.count(' ') + 1}`")
            
            # Bouton pour voir plus
            if st.button("Voir l'article complet", key=f"wiki_{page.title}"):
                st.write(page.text)
    else:
        st.warning(f"Aucune page Wikipédia trouvée pour '{search_term}' en {language}.")

def search_external_sources(term):
    """Recherche dans DuckDuckGo"""
    st.subheader("🌐 Résultats d'autres sources")
    url = f"https://html.duckduckgo.com/html/?q={term}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        with st.spinner("Recherche en cours..."):
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("a", class_="result__a", limit=max_results)

        if results:
            for i, link in enumerate(results, start=1):
                with st.container(border=True):
                    st.markdown(f"**{i}. [{link.get_text(strip=True)}]({link['href']})**")
                    # Essayer d'extraire un extrait de description si disponible
                    next_sibling = link.find_next(class_="result__snippet")
                    if next_sibling:
                        st.caption(next_sibling.get_text(strip=True))
        else:
            st.info("Aucun résultat externe trouvé.")
    except Exception as e:
        st.error(f"Erreur lors de la recherche externe: {e}")

# Exécution de la recherche
if search_term:
    st.divider()
    st.header(f"Résultats pour: '{search_term}'")
    
    # Recherche Wikipédia
    page = wiki.page(search_term)
    display_wiki_info(page)
    
    # Recherche externe si pas de résultat Wikipédia ou si demandé
    if not page.exists() or st.checkbox("Afficher aussi les résultats externes même avec un résultat Wikipédia"):
        search_external_sources(search_term)
else:
    st.info("Veuillez entrer un terme de recherche pour commencer.")

# Pied de page
st.divider()
st.caption("Application développée avec Streamlit - Moteur de recherche utilisant Wikipédia et DuckDuckGo")