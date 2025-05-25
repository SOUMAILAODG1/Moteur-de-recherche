import streamlit as st
import wikipediaapi
import requests
from bs4 import BeautifulSoup
from datetime import date

st.set_page_config(page_title="Moteur de Recherche Multisource", layout="wide")

# ===== En-tête avec logos et titre principal =====
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.image("Logo_Université_de_Ouagadougou-292x300.jpg", width=100)
with col2:
    st.markdown("<h3 style='text-align: center;'>Master 2 en Ingeneirie Logicielle et Systeme d'Information Informayisée</h3>", unsafe_allow_html=True)
    
    st.markdown("<h4 style='text-align: center;'>Projet de Conception d'un Moteur de Recherche d'Information</h4>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center;'>Concepteur Soumaila OUEDRAOGO", unsafe_allow_html=True)
with col3:
    st.image("ufrsea.png", width=100)

st.markdown("<h2 style='text-align:center;'>🔍 Moteur de Recherche Multisource</h2>", unsafe_allow_html=True)

# ===== Zone de recherche =====
search_term = st.text_input("Entrez votre recherche...", "")

# ===== Filtres =====
with st.expander("🔧 Filtres avancés"):
    st.markdown("### Filtres")
    score_min = st.number_input("Score minimum:", min_value=0, value=0)
    date_min = st.date_input("Date après:", value=date.today())
    sort_by = st.selectbox("Trier par:", ["Pertinence", "Date"])

# ===== Paramètres dans la sidebar =====
with st.sidebar:
    st.header("Paramètres")
    language = st.selectbox("Langue Wikipédia", ["fr", "en", "es", "de"], index=0)
    max_results = st.slider("Nombre max de résultats externes", 1, 10, 5)

# ===== Fonctions de recherche =====
wiki = wikipediaapi.Wikipedia(language=language, user_agent='MonMoteurRechercheRI/1.0 (contact@example.com)')

def display_wiki_info(page):
    if page.exists():
        with st.container(border=True):
            st.subheader(f"📖 {page.title} (Wikipédia)")
            st.write(f"**Résumé:** {page.summary[:500]}...")
            st.write(f"**URL:** {page.fullurl}")
            st.caption(f"Langue: {page.language} — Mots: {page.text.count(' ') + 1}")
            if st.button("Voir l'article complet", key=f"wiki_{page.title}"):
                st.write(page.text)
    else:
        st.warning(f"Aucune page Wikipédia trouvée pour '{search_term}' en {language}.")

def search_external_sources(term):
    st.subheader("🌐 Résultats externes (DuckDuckGo)")
    url = f"https://html.duckduckgo.com/html/?q={term}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        with st.spinner("Recherche en cours..."):
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("a", class_="result__a", limit=max_results)
        if results:
            for i, link in enumerate(results, 1):
                with st.container(border=True):
                    st.markdown(f"**{i}. [{link.get_text(strip=True)}]({link['href']})**")
                    snippet = link.find_next(class_="result__snippet")
                    if snippet:
                        st.caption(snippet.get_text(strip=True))
        else:
            st.info("Aucun résultat externe trouvé.")
    except Exception as e:
        st.error(f"Erreur : {e}")

# ===== Recherche =====
if search_term:
    st.divider()
    st.header(f"Résultats pour: '{search_term}'")
    page = wiki.page(search_term)
    display_wiki_info(page)
    if not page.exists() or st.checkbox("Afficher aussi les résultats externes"):
        search_external_sources(search_term)
else:
    st.info("Veuillez entrer un terme de recherche.")

# ===== Section : Ajout de documents (crawler) =====
st.divider()
st.subheader("📄 Ajouter des documents")
with st.form("add_docs"):
    url = st.text_input("URL de départ:")
    max_pages = st.number_input("Nombre maximum de pages:", min_value=1, value=100)
    submitted = st.form_submit_button("Lancer le crawler")
    if submitted:
        st.success("Crawler lancé (simulation).")

# ===== Statistiques =====
st.subheader("📊 Statistiques")
col_a, col_b = st.columns(2)
col_a.metric("Documents indexés", "0")
col_b.metric("Taille du cache", "2")

# ===== Pied de page =====
st.divider()
st.markdown("""
    <div style='text-align: center; font-size: 0.9em;'>
        AUTEUR SOUMAILA OUEDRAOGO<br/>
    </div>
""", unsafe_allow_html=True)
