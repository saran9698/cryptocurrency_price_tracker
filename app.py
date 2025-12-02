import streamlit as st
import pandas as pd
import time
from datetime import datetime
from scraper import scrape_top_coins  

st.set_page_config(page_title="💰 Crypto Tracker", layout="wide")
st.title("💰 Real-Time Cryptocurrency Price Tracker")

st.sidebar.header("⚙️ Controls")
limit = st.sidebar.slider("Number of top coins to display", 5, 100, 10, 5)
auto_refresh = st.sidebar.checkbox("⏱️ Auto-refresh every 5 mins", value=True)
refresh_button = st.sidebar.button("🔄 Refresh Now")

table_placeholder = st.empty()
timestamp_placeholder = st.empty()

def get_data():
    df = scrape_top_coins(limit=limit, headless=True)
    return df

def display_data():
    df = get_data()
    table_placeholder.dataframe(df)
    timestamp_placeholder.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

display_data()

if refresh_button:
    display_data()

if auto_refresh:
    while True:
        time.sleep(300)  
        display_data()
        st.experimental_rerun()
