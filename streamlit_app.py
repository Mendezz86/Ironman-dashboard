import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# --- Designinställningar ---
st.set_page_config(page_title="Ironman Kalmar 2026", layout="wide", initial_sidebar_state="expanded")

# --- Stilren Custom CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #e2e8f0; }
    .hero-metric {
        background-color: #1a202c;
        padding: 20px;
        border-radius: 12px;
        border-bottom: 4px solid #3b82f6;
        text-align: center;
        margin-bottom: 15px;
    }
    .hero-label { color: #94a3b8; font-size: 13px; text-transform: uppercase; font-weight: 600; }
    .hero-value { color: #ffffff; font-size: 28px; font-weight: 700; margin-top: 5px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTION: Bearbeta Garmin CSV ---
def process_data(file):
    df = pd.read_csv(file)
    # Hanterar distans (ersätter komma med punkt och tar bort bindestreck)
    if 'Distans' in df.columns:
        df['Distans'] = df['Distans'].astype(str).str.replace(',', '.').replace('--', '0').astype(float)
    if 'Datum' in df.columns:
        df['Datum'] = pd.to_datetime(df['Datum'])
    return df

# --- SIDOPANEL (Endast Data) ---
with st.sidebar:
    st.title("📊 Data Center")
    st.write("Ladda upp din senaste export från Garmin Connect för att uppdatera din analys.")
    uploaded_file = st.file_uploader("Välj Activities.csv", type="csv")
    
    if uploaded_file:
        st.success("Data laddad!")

# --- HEADER ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🏆 Ironman Dashboard")
    st.caption("Fokus: Kalmar 2026")
with col_h2:
    days_left = (date(2026, 8, 15) - date.today()).days
    st.metric("Dagar till start", f"{days_left}")

# --- LOGIK FÖR DATA ---
if uploaded_file:
    data = process_data(uploaded_file)
    latest_run = data[data['Aktivitetstyp'].str.contains('Löpning|Landsvägslöpning', na=False, case=False)].iloc[0] if not data.empty else None
    latest_bike = data[data['Aktivitetstyp'].str.contains('Cykling|Virtuell cykling', na=False, case=False)].iloc[0] if not data.empty else None
    latest_swim = data[data['Aktivitetstyp'].str.contains('Simning|Simbassäng', na=False, case=False)].iloc[0] if not data.empty else None
else:
    data = None

# --- FLIK-SYSTEMET ---
tab_form, tab_cykel, tab_lop, tab_sim = st.tabs(["🩺 Dagsform", "🚴 Cykel", "🏃 Löpning", "🏊 Simning"])

with tab_form:
    st.header("Träningsvolym")
    if data is not None:
        # Visar distans över tid för de senaste 15 passen
        volume_chart = data.head(15)[['Datum', 'Distans']].set_index('Datum')
        st.bar_chart(volume_chart)
    else:
        st.info("Väntar på data... Ladda upp din Activities.csv i sidopanelen.")

with tab_cykel:
    st.header("Senaste Cykelpass")
    if data is not None and latest_bike is not None:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"""<div class="hero-metric"><div class="hero-label">NP® Watt</div><div class="hero-value">{latest_bike.get('Normalized Power® (NP®)', '--')} W</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown(f"""<div class="hero-metric"><div class="hero-label">Distans</div><div class="hero-value">{latest_bike.get('Distans', '--')} km</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown(f"""<div class="hero-metric"><div class="hero-label">TSS®</div><div class="hero-value">{latest_bike.get('Training Stress Score®', '--')}</div></div>""", unsafe_allow_html=True)
    else:
        st.warning("Ingen cykeldata hittad i filen.")

with tab_lop:
    st.header("Löpdynamik")
    if data is not None and latest_run is not None:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"""<div class="hero-metric" style="border-bottom-color: #ef4444;"><div class="hero-label">Markkontakttid</div><div class="hero-value">{latest_run.get('Medeltid för markkontakt', '--')} ms</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown(f"""<div class="hero-metric" style="border-bottom-color: #ef4444;"><div class="hero-label">Balans</div><div class="hero-value">{latest_run.get('Medelkontakttidsbalans', '--')}</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown(f"""<div class="hero-metric" style="border-bottom-color: #ef4444;"><div class="hero-label">Kadens</div><div class="hero-value">{latest_run.get('Medellöpkadens', '--')} spm</div></div>""", unsafe_allow_html=True)
    else:
        st.warning("Ingen löpdata hittad i filen.")

with tab_sim:
    st.header("Sim
