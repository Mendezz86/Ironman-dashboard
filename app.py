import streamlit as st
from datetime import date
from garminconnect import Garmin
import os
import garth
import pandas as pd
import numpy as np

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
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-size: 16px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDOPANEL ---
with st.sidebar:
    st.title("⚙️ Garmin Sync")
    email = st.text_input("E-post")
    password = st.text_input("Lösenord", type="password")
    sync_clicked = st.button("Hämta senaste pass")
    
    st.divider()
    st.subheader("📝 Checklista")
    st.checkbox("Växla 50 USD för visum", value=False)
    st.checkbox("Se över budget för dricks", value=False)
    st.checkbox("Boka cykeltransport", value=False)

# --- HEADER ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🏆 Min Resa mot Ironman")
with col_h2:
    race_day = date(2026, 8, 15)
    days_left = (race_day - date.today()).days
    st.metric("Dagar till start", f"{days_left} kvar")

st.write("---")

# --- FLIK-SYSTEMET ---
tab_form, tab_cykel, tab_lop, tab_sim = st.tabs(["🩺 Dagsform", "🚴 Cykelanalys", "🏃 Löpanalys", "🏊 Simanalys"])

# === FLIK 1: DAGSFORM & HÄLSA ===
with tab_form:
    st.header("Återhämtning & Beredskap")
    if sync_clicked:
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown("""<div class="hero-metric" style="border-bottom-color: #10b981;"><div class="hero-label">Träningsberedskap</div><div class="hero-value">84 / 100</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown("""<div class="hero-metric" style="border-bottom-color: #3b82f6;"><div class="hero-label">Body Battery</div><div class="hero-value">72 %</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown("""<div class="hero-metric" style="border-bottom-color: #8b5cf6;"><div class="hero-label">Sömnpoäng</div><div class="hero-value">88</div></div>""", unsafe_allow_html=True)
        with c4: st.markdown("""<div class="hero-metric" style="border-bottom-color: #f59e0b;"><div class="hero-label">HRV (Natt)</div><div class="hero-value">65 ms</div></div>""", unsafe_allow_html=True)
    else:
        st.info("Synka för att se din dagsform.")

    st.subheader("📅 Planering & Volym")
    chart_data = pd.DataFrame(np.random.uniform(5, 15, size=(10, 3)), columns=["Sim", "Cykel", "Löp"], index=[f"v.{i}" for i in range(10, 20)])
    st.bar_chart(chart_data, height=250)

# === FLIK 2: CYKELANALYS ===
with tab_cykel:
    st.header("Kraft & Prestation")
    if sync_clicked:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("""<div class="hero-metric"><div class="hero-label">Normalized Power® (NP)</div><div class="hero-value">215 W</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown("""<div class="hero-metric"><div class="hero-label">Training Stress Score®</div><div class="hero-value">142 TSS</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown("""<div class="hero-metric"><div class="hero-label">Maxkraft (20 min)</div><div class="hero-value">245 W</div></div>""", unsafe_allow_html=True)
        
        st.subheader("Utrustning: Trek Speed Concept")
        st.progress(100)
        st.caption("Status: Grön (Nyservad)")
    else:
        st.info("Synka för att se dina cykelwatt.")

# === FLIK 3: LÖPANALYS ===
with tab_lop:
    st.header("Löpdynamik & Effektivitet")
    if sync_clicked:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("""<div class="hero-metric" style="border-bottom-color: #ef4444;"><div class="hero-label">Kontakttidsbalans</div><div class="hero-value">49.8% L / 50.2% R</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown("""<div class="hero-metric" style="border-bottom-color: #ef4444;"><div class="hero-label">Vertikal Rörelse</div><div class="hero-value">8.2 cm</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown("""<div class="hero-metric" style="border-bottom-color: #ef4444;"><div class="hero-label">VO2 Max (Löpning)</div><div class="hero-value">54</div></div>""", unsafe_allow_html=True)
        
        st.subheader("Utrustning: Saucony Endorphin")
        shoe_km = 850
        st.progress(shoe_km / 1200)
        st.caption(f"{shoe_km} / 1200 km (Gul varning)")
    else:
        st.info("Synka för att se din löpteknik.")

# === FLIK 4: SIMANALYS ===
with tab_sim:
    st.header("Teknik i vattnet")
    if sync_clicked:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("""<div class="hero-metric" style="border-bottom-color: #0ea5e9;"><div class="hero-label">Medel-Swolf</div><div class="hero-value">34</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown("""<div class="hero-metric" style="border-bottom-color: #0ea5e9;"><div class="hero-label">Simkadens</div><div class="hero-value">28 drag/min</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown("""<div class="hero-metric" style="border-bottom-color: #0ea5e9;"><div class="hero-label">Distans</div><div class="hero-value">2800 m</div></div>""", unsafe_allow_html=True)
    else:
        st.info("Synka för att se din simdata.")