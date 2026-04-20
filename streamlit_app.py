import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# --- Designinställningar ---
st.set_page_config(page_title="IRONMAN KALMAR 2026", layout="wide", initial_sidebar_state="expanded")

# --- Avancerad Custom CSS för "Ironman-look" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&display=swap');
    
    .main { background-color: #0e1117; color: #e2e8f0; }
    
    /* Branding Header */
    .ironman-header {
        text-align: center;
        padding: 40px 0px;
        background: linear-gradient(180deg, rgba(239,68,68,0.1) 0%, rgba(14,17,23,0) 100%);
        border-radius: 20px;
        margin-bottom: 30px;
    }
    
    .ironman-logo-text {
        font-family: 'Oswald', sans-serif;
        font-size: 64px;
        font-weight: 700;
        letter-spacing: 4px;
        color: #ffffff;
        text-transform: uppercase;
        margin: 0;
        text-shadow: 0 0 20px rgba(239, 68, 68, 0.6);
    }
    
    .ironman-sub {
        color: #ef4444;
        letter-spacing: 8px;
        font-size: 14px;
        font-weight: 600;
        margin-top: -10px;
    }

    /* Mätar-kort */
    .hero-metric {
        background-color: #1a202c;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #2d3748;
        border-bottom: 4px solid #ef4444;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .hero-metric:hover {
        transform: translateY(-5px);
        border-color: #ef4444;
    }
    .hero-label { color: #94a3b8; font-size: 12px; text-transform: uppercase; font-weight: 600; letter-spacing: 1px; }
    .hero-value { color: #ffffff; font-size: 32px; font-weight: 700; margin-top: 5px; }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTION: Bearbeta Garmin CSV ---
def process_data(file):
    try:
        df = pd.read_csv(file)
        if 'Distans' in df.columns:
            df['Distans'] = df['Distans'].astype(str).str.replace(',', '.').replace('--', '0').astype(float)
        if 'Datum' in df.columns:
            df['Datum'] = pd.to_datetime(df['Datum'])
        return df
    except:
        return None

# --- SIDOPANEL ---
with st.sidebar:
    # Här kan du också lägga en mindre logga
    st.markdown("<h2 style='text-align: center; color: #ef4444;'>ANYTHING IS POSSIBLE</h2>", unsafe_allow_html=True)
    st.divider()
    uploaded_file = st.file_uploader("Uppdatera analys med Activities.csv", type="csv")
    if uploaded_file:
        st.success("Data synkad!")

# --- COOL HEADER SECTION ---
st.markdown("""
    <div class="ironman-header">
        <p class="ironman-logo-text">IRONMAN</p>
        <p class="ironman-sub">KALMAR 2026</p>
    </div>
    """, unsafe_allow_html=True)

# --- NEDRÄKNING ---
col_empty, col_countdown, col_empty2 = st.columns([1, 2, 1])
with col_countdown:
    days_left = (date(2026, 8, 15) - date.today()).days
    st.metric("", f"{days_left} DAGAR TILL START", help="Nedräkning till Kalmar Ironman 2026")

st.write("---")

# --- LOGIK FÖR DATA ---
if uploaded_file:
    data = process_data(uploaded_file)
    latest_run = data[data['Aktivitetstyp'].str.contains('Löpning|Landsvägslöpning', na=False, case=False)].iloc[0] if not data.empty else None
    latest_bike = data[data['Aktivitetstyp'].str.contains('Cykling|Virtuell cykling', na=False, case=False)].iloc[0] if not data.empty else None
    latest_swim = data[data['Aktivitetstyp'].str.contains('Simning|Simbassäng', na=False, case=False)].iloc[0] if not data.empty else None
else:
    data = None

# --- FLIK-SYSTEMET ---
tab_form, tab_cykel, tab_lop, tab_sim = st.tabs(["🩺 DAGSFORM", "🚴 CYKEL", "🏃 LÖPNING", "🏊 SIMNING"])

# (Resten av logiken för tab-innehåll stannar som förut, men med uppdaterad styling)
with tab_form:
    if data is not None:
        st.subheader("Träningsvolym (Senaste passen)")
        volume_chart = data.head(15)[['Datum', 'Distans']].set_index('Datum')
        st.bar_chart(volume_chart, color="#ef4444")
    else:
        st.info("Ladda upp data för att se din formtrend.")

with tab_cykel:
    if data is not None and latest_bike is not None:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="hero-metric"><div class="hero-label">NP® WATT</div><div class="hero-value">{latest_bike.get("Normalized Power® (NP®)", "--")}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="hero-metric"><div class="hero-label">DISTANS</div><div class="hero-value">{latest_bike.get("Distans", "--")} km</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="hero-metric"><div class="hero-label">TSS®</div><div class="hero-value">{latest_bike.get("Training Stress Score®", "--")}</div></div>', unsafe_allow_html=True)
    else:
        st.warning("Ingen cykeldata.")

with tab_lop:
    if data is not None and latest_run is not None:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="hero-metric"><div class="hero-label">MARKKONTAKT</div><div class="hero-value">{latest_run.get("Medeltid för markkontakt", "--")} ms</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="hero-metric"><div class="hero-label">BALANS</div><div class="hero-value">{latest_run.get("Medelkontakttidsbalans", "--")}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="hero-metric"><div class="hero-label">KADENS</div><div class="hero-value">{latest_run.get("Medellöpkadens", "--")}</div></div>', unsafe_allow_html=True)

with tab_sim:
    if data is not None and latest_swim is not None:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="hero-metric"><div class="hero-label">SWOLF</div><div class="hero-value">{latest_swim.get("Medel-Swolf", "--")}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="hero-metric"><div class="hero-label">TEMPO</div><div class="hero-value">{latest_swim.get("Medeltempo", "--")}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="hero-metric"><div class="hero-label">STRÄCKA</div><div class="hero-value">{latest_swim.get("Distans", "--")} m</div></div>', unsafe_allow_html=True)
