import streamlit as st
import undetected_chromedriver as uc
import time

def create_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')

    driver = uc.Chrome(options=options)
    return driver

def scrape_title(url):
    driver = create_driver()
    driver.get(url)
    time.sleep(2)
    
    title = driver.title
    driver.quit()
    return title

st.title("🔎 Streamlit + Selenium (Undetected Chrome)")

url = st.text_input("Masukkan URL:")

if st.button("Scrape Title"):
    if url:
        with st.spinner("Scraping..."):
            title = scrape_title(url)
            st.success(f"Judul Halaman: {title}")
    else:
        st.warning("Masukkan URL terlebih dahulu.")
