import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ⚙️ Configuration de la page
st.set_page_config(page_title="📊 Mini App Data Pro", layout="wide")
st.title("📊 Mini Application d’Analyse de Données")

# 📂 Upload CSV
uploaded_file = st.file_uploader("📥 Importer un fichier CSV", type="csv")

if uploaded_file:
    # Charger les données
    df = pd.read_csv(uploaded_file)
    st.success("✅ Fichier chargé avec succès !")
    
    # 📋 Aperçu des données
    with st.expander("👀 Aperçu du dataset"):
        st.dataframe(df.head(20))

    # 🔎 Infos générales
    st.subheader("📌 Informations générales")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de lignes", df.shape[0])
    col2.metric("Nombre de colonnes", df.shape[1])
    col3.metric("Colonnes numériques", len(df.select_dtypes(include='number').columns))

    # 🧮 Sélection colonne numérique
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) > 0:
        colonne = st.selectbox("Choisir une colonne numérique", numeric_cols)

        # 📊 Options de visualisation
        st.subheader("📊 Visualisations")
        graph_type = st.radio("Type de graphique", ["Histogramme", "Boxplot", "Nuage de points (Scatter)"])

        if graph_type == "Histogramme":
            fig, ax = plt.subplots(figsize=(8,4))
            sns.histplot(df[colonne], kde=True, color='skyblue', ax=ax)
            st.pyplot(fig)

        elif graph_type == "Boxplot":
            fig, ax = plt.subplots(figsize=(6,3))
            sns.boxplot(x=df[colonne], color='lightcoral', ax=ax)
            st.pyplot(fig)

        elif graph_type == "Nuage de points (Scatter)":
            other_num = st.selectbox("Choisir une autre colonne numérique", [c for c in numeric_cols if c != colonne])
            fig = px.scatter(df, x=colonne, y=other_num, color=df.select_dtypes(include='object').columns[0] if len(df.select_dtypes(include='object').columns) > 0 else None)
            st.plotly_chart(fig, use_container_width=True)

        # 📈 Statistiques descriptives
        st.subheader(f"📈 Statistiques sur {colonne}")
        desc = df[colonne].describe().to_frame()
        st.table(desc)

    else:
        st.warning("⚠️ Aucune colonne numérique trouvée dans ce fichier CSV.")

    # 🔍 Recherche et filtrage
    st.subheader("🔍 Filtrer les données")
    colonne_filtre = st.selectbox("Choisir une colonne pour filtrer", df.columns)
    valeur = st.text_input(f"Filtrer sur {colonne_filtre}")
    if valeur:
        st.write(df[df[colonne_filtre].astype(str).str.contains(valeur, case=False)])

    # 📤 Télécharger les données nettoyées
    st.subheader("📤 Exporter les données")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Télécharger le dataset", csv, "donnees.csv", "text/csv")
