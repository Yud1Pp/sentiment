import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    chrome_options.binary_location = '/usr/bin/chromium'
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def take_screenshot(url, filename="screenshot.png"):
    driver = create_driver()
    driver.get(url)
    time.sleep(2)

    # Simpan screenshot ke file
    driver.save_screenshot(filename)
    driver.quit()
    return filename

st.title("🔎 Streamlit + Selenium (Chromium)")

url = st.text_input("Masukkan URL:")

if st.button("Ambil Screenshot"):
    if url:
        with st.spinner("Mengambil screenshot..."):
            screenshot_path = take_screenshot(url)
            if os.path.exists(screenshot_path):
                st.image(screenshot_path, caption="Screenshot halaman", use_column_width=True)
                st.success("Screenshot berhasil diambil.")
            else:
                st.error("Gagal mengambil screenshot.")
    else:
        st.warning("Masukkan URL terlebih dahulu.")
