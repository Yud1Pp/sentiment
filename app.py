import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    chrome_options.binary_location = '/usr/bin/chromium'

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def scrape_title(url):
    driver = create_driver()
    driver.get(url)
    time.sleep(2)
    
    title = driver.title
    driver.quit()
    return title

st.title("🔎 Streamlit + Selenium (Chromium)")

url = st.text_input("Masukkan URL:")

if st.button("Scrape Title"):
    if url:
        with st.spinner("Scraping..."):
            title = scrape_title(url)
            st.success(f"Judul Halaman: {title}")
    else:
        st.warning("Masukkan URL terlebih dahulu.")
