import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Energy Agent",
    page_icon="⚡",
    layout="wide"
)

# Chargement des données
df = pd.read_csv("agent_decisions.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Titre
st.title("⚡ Smart Energy Consumption Advisory Agent")
st.caption("Analyse, prédiction et recommandations énergétiques")

# Indicateurs
total = len(df)
normal = (df["decision"] == "NORMAL").sum()
anomalies = df["is_anomaly"].sum()
risks = df["high_consumption"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total des mesures", f"{total:,}")
col2.metric("Situations normales", f"{normal:,}")
col3.metric("Anomalies détectées", f"{anomalies:,}")
col4.metric("Alertes de consommation", f"{risks:,}")

st.divider()

# Consommation réelle et prédite
st.subheader("📈 Consommation réelle et prédite")

chart_data = df.set_index("timestamp")[
    ["global_active_power", "predicted_next"]
]

st.line_chart(chart_data)

st.divider()

# Répartition des décisions
st.subheader("📊 Répartition des décisions")

st.bar_chart(df["decision"].value_counts())

st.divider()

# Consultation des recommandations
st.subheader("🔎 Explorer les décisions")

selected_decision = st.selectbox(
    "Choisir une catégorie",
    ["Toutes"] + sorted(df["decision"].unique().tolist())
)

if selected_decision == "Toutes":
    filtered_df = df
else:
    filtered_df = df[df["decision"] == selected_decision]

st.dataframe(
    filtered_df[
        ["timestamp", "global_active_power", "predicted_next",
         "decision", "recommendation", "explanation"]
    ],
    use_container_width=True
)
