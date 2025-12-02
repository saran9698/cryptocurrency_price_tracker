import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_top_coins(limit=10, headless=True):
   
    url = "https://coinmarketcap.com/"
    driver = get_driver(headless)
    driver.get(url)
    time.sleep(10) 

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    rank, name, symbol, buy_sell, price, change_24h, market_cap = [], [], [], [], [], [], []

    for r in rows[:limit]:
        try:
            cols = r.text.split("\n")
            if len(cols) >= 8:
                rank.append(cols[0])
                name.append(cols[1])
                symbol.append(cols[2])
                buy_sell_val = "Buy" if "Buy" in cols[3] else "Sell" if "Sell" in cols[3] else ""
                buy_sell.append(buy_sell_val)
                price.append(cols[4])
                change_24h.append(cols[5])
                market_cap.append(cols[7])
        except:
            continue

    driver.quit()

    df = pd.DataFrame({
        "rank": rank,
        "name": name,
        "symbol": symbol,
        "buy": buy_sell,
        "price": price,
        "1h 24h 7d_change": change_24h,
        "marketcap": market_cap,
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(rank)
    })

    return df

def save_data(df, filename="crypto_data.csv"):
    os.makedirs("data", exist_ok=True)
    if not df.empty:
        df.to_csv(filename, index=False, mode='a', header=not os.path.exists(filename))
        print(f"✅ Data saved to {filename}")
    else:
        print("⚠️ No data scraped")

if __name__ == "__main__":
    df = scrape_top_coins(limit=10, headless=True)
    print(df.to_string(index=False))
    save_data(df)
