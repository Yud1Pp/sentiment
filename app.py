import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time

def create_driver():
    # Install ChromeDriver yang cocok secara otomatis
    chromedriver_autoinstaller.install()
    
    options = Options()
    options.add_argument('--headless')  # Jalankan dalam mode headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_title(url):
    driver = create_driver()
    driver.get(url)
    time.sleep(2)  # Tunggu 2 detik biar halaman load
    
    title = driver.title  # Ambil title halaman
    driver.quit()
    return title

st.title("🔎 Streamlit + Selenium Demo")

url = st.text_input("Masukkan URL untuk scraping:")

if st.button("Scrape Title"):
    if url:
        with st.spinner("Scraping..."):
            title = scrape_title(url)
            st.success(f"Judul Halaman: {title}")
    else:
        st.warning("Mohon masukkan URL terlebih dahulu.")
