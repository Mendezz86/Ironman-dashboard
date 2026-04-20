import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta

# --- Designinställningar ---
st.set_page_config(page_title="IRONMAN KALMAR 2026", layout="wide", initial_sidebar_state="expanded")

# --- Avancerad Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&display=swap');
    .main { background-color: #0e1117; color: #e2e8f0; }
    
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
    
    .ironman-sub { color: #ef4444; letter-spacing: 8px; font-size: 14px; font-weight: 600; margin-top: -10px; }

    .hero-metric {
        background-color: #1a202c;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #2d3748;
        border-bottom: 4px solid #ef4444;
        text-align: center;
    }
    .hero-label { color: #94a3b8; font-size: 12px; text-transform: uppercase; font-weight: 600; }
    .hero-value { color: #ffffff; font-size: 32px; font-weight: 700; margin-top: 5px; }
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
    st.markdown("<h2 style='text-align: center; color: #ef4444;'>ANYTHING IS POSSIBLE</h2>", unsafe_allow_html=True)
    st.divider()
    uploaded_file = st.file_uploader("Ladda upp Activities.csv", type="csv")

# --- HEADER ---
st.markdown('<div class="ironman-header"><p class="ironman-logo-text">IRONMAN</p><p class="ironman-sub">KALMAR 2026</p></div>', unsafe_allow_html=True)

# --- LOGIK FÖR DATA ---
if uploaded_file:
    data = process_data(uploaded_file)
    if data is not None:
        latest_run = data[data['Aktivitetstyp'].str.contains('Löpning|Landsvägslöpning', na=False, case=False)].iloc[0] if not data.empty else None
        latest_bike = data[data['Aktivitetstyp'].str.contains('Cykling|Virtuell cykling', na=False, case=False)].iloc[0] if not data.empty else None
        latest_swim = data[data['Aktivitetstyp'].str.contains('Simning|Simbassäng', na=False, case=False)].iloc[0] if not data.empty else None
        
        data['Vecka'] = data['Datum'].dt.isocalendar().week
        current_week = date.today().isocalendar()[1]
        weekly_data = data[data['Vecka'] > (current_week - 5)]
        
        def get_weekly_sum(activity_filter):
            subset = weekly_data[weekly_data['Aktivitetstyp'].str.contains(activity_filter, na=False, case=False)]
            return subset.groupby('Vecka')['Distans'].sum()

        # Konvertera simning från km till meter i grafen
        swim_vol = get_weekly_sum('Simning|Simbassäng') * 1000
        bike_vol = get_weekly_sum('Cykling|Virtuell cykling')
        run_vol = get_weekly_sum('Löpning|Landsvägslöpning')
    else:
        latest_run = latest_bike = latest_swim = None
else:
    data = None

# --- FLIKAR ---
tab_form, tab_cykel, tab_lop, tab_sim = st.tabs(["🩺 DAGSFORM", "🚴 CYKEL", "🏃 LÖPNING", "🏊 SIMNING"])

with tab_form:
    if data is not None:
        st.subheader("Veckovolym (Senaste veckorna)")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("**Simning (m)**")
            st.bar_chart(swim_vol, color="#0ea5e9")
        with c2:
            st.write("**Cykling (km)**")
            st.bar_chart(bike_vol, color="#ef4444")
        with c3:
            st.write("**Löpning (km)**")
            st.bar_chart(run_vol, color="#f59e0b")
    else:
        st.info("Ladda upp din fil för att se din progression.")

with tab_cykel:
    if data is not None and latest_bike is not None:
        st.subheader(f"Senaste passet: {latest_bike['Datum'].date()}")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="hero-metric"><div class="hero-label">NP® WATT</div><div class="hero-value">{latest_bike.get("Normalized Power® (NP®)", "--")}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="hero-metric"><div class="hero-label">DISTANS</div><div class="hero-value">{latest_bike.get("Distans", "--")} km</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="hero-metric"><div class="hero-label">TSS®</div><div class="hero-value">{latest_bike.get("Training Stress Score®", "--")}</div></div>', unsafe_allow_html=True)

with tab_lop:
    if data is not None and latest_run is not None:
        st.subheader(f"Senaste passet: {latest_run['Datum'].date()}")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="hero-metric" style="border-bottom-color: #f59e0b;"><div class="hero-label">MARKKONTAKT</div><div class="hero-value">{latest_run.get("Medeltid för markkontakt", "--")} ms</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="hero-metric" style="border-bottom-color: #f59e0b;"><div class="hero-label">BALANS</div><div class="hero-value">{latest_run.get("Medelkontakttidsbalans", "--")}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="hero-metric" style="border-bottom-color: #f59e0b;"><div class="hero-label">KADENS</div><div class="hero-value">{latest_run.get("Medellöpkadens", "--")} spm</div></div>', unsafe_allow_html=True)

with tab_sim:
    if data is not None and latest_swim is not None:
        st.subheader(f"Senaste passet: {latest_swim['Datum'].date()}")
        # Konvertera distans till meter för visning
        swim_dist = latest_swim.get("Distans", 0)
        swim_m = int(float(swim_dist) * 1000) if swim_dist != "--" else "--"
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="hero-metric" style="border-bottom-color: #0ea5e9;"><div class="hero-label">SWOLF</div><div class="hero-value">{latest_swim.get("Medel-Swolf", "--")}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="hero-metric" style="border-bottom-color: #0ea5e9;"><div class="hero-label">TEMPO</div><div class="hero-value">{latest_swim.get("Medeltempo", "--")}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="hero-metric" style="border-bottom-color: #0ea5e9;"><div class="hero-label">STRÄCKA</div><div class="hero-value">{swim_m} m</div></div>', unsafe_allow_html=True)
