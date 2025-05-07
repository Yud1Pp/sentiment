from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import streamlit as st

class TokopediaScraper:
    def __init__(self, url, max_per_rating=50):
        self.url = url
        self.max_per_rating = max_per_rating
        self.isCheckbox = False
        self.cntCheckEnb = 0
    
    def create_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0")
        
        options.binary_location = '/usr/bin/chromium'

        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)
        
        return driver

    def click_checkbox(self, driver, rating):
        labels = driver.find_elements(By.CSS_SELECTOR, "label.checkbox")
        for label in labels:
            try:
                p = label.find_element(By.TAG_NAME, "p")
                if p.text.strip() == str(rating):
                    # Cek apakah input checkbox di dalam label dalam kondisi disabled
                    try:
                        checkbox_input = label.find_element(By.TAG_NAME, "input")
                        if checkbox_input.get_attribute("disabled") is not None:
                            print(f"Rating {rating} checkbox dalam kondisi disabled.")
                            return None  # Jika disabled, skip checkbox ini
                    except:
                        continue
                    return label
            except:
                continue
        return None

    def scrape_and_analyze(self):
        st.write("haiii")
        driver = self.create_driver()
        data_review = []
        try:
            driver.set_window_size(1300, 800)
            driver.get(self.url)
            time.sleep(3)
            test = driver.find_element(By.CLASS_NAME, "css-11hzwo5").get_attribute("outerHTML")
            st.write(f"Url: {self.url}")
            st.write(f"hallo: {test}")
            

            # Tutup popup jika muncul
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "css-11hzwo5"))
                ).find_element(By.TAG_NAME, "button").click()
            except:
                pass

            # Scroll dan buka bagian review
            for _ in range(10):
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(1)
                try:
                    WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "css-evcn9a"))
                    ).click()
                    break
                except:
                    continue

            # Urutkan berdasarkan terbaru
            try:
                tombol_urutkan = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="reviewSorting"]')
                if tombol_urutkan.is_enabled():
                    print("urutkan terpencet")
                    # Scroll dan tunggu tombol bisa diklik
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tombol_urutkan)
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="reviewSorting"]')))
                    tombol_urutkan.click()
                    
                    tombol_terbaru = driver.find_element(By.CSS_SELECTOR, 'button[data-item-text="Terbaru"]')
                    print(tombol_terbaru.get_attribute("outerHTML"))
                    if tombol_terbaru.is_enabled():
                    # Scroll dan tunggu tombol bisa diklik
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tombol_terbaru)
                        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-item-text="Terbaru"]')))
                        tombol_terbaru.click()
            except:
                print("Tombol urutkan tidak ditemukan atau tidak dapat diklik.")
# https://www.tokopedia.com/belle-baby-store/sgm-ananda-sgm-eksplor-1-sgm-eksplor-3-vanila-madu-900gr-belle-baby-store-bubuk-bunda-1730453605551277186?t_id=1746500217695&t_st=6&t_pp=homepage&t_efo=pure_goods_card&t_ef=homepage&t_sm=rec_homepage_outer_flow&t_spt=homepage
            # Mulai scraping review per rating
            for rating in [5, 4, 3, 2, 1]:
                checkbox = self.click_checkbox(driver, rating)
                if not checkbox:
                    print(f"Rating {rating} tidak tersedia di checkbox.")
                    self.isCheckbox = False
                    self.cntCheckEnb += 1
                    continue  # Jika checkbox untuk rating ini tidak ada, lanjutkan ke rating berikutnya
                
                try:
                    self.isCheckbox = True
                    area = checkbox.find_element(By.CLASS_NAME, "css-4iffx4-unf-checkbox__area")
                    area.click()  # Klik checkbox
                except:
                    checkbox.click()
                time.sleep(2)

                collected = 0
                while collected < self.max_per_rating:
                    reviews = driver.find_elements(By.CSS_SELECTOR, "article.css-15m2bcr")
                    for el in reviews:
                        try:
                            tombol = el.find_element(By.CSS_SELECTOR, "button.css-89c2tx")
                            driver.execute_script("arguments[0].click();", tombol)
                            time.sleep(0.2)
                        except:
                            pass
                        try:
                            nama = el.find_element(By.CLASS_NAME, "name").text
                        except:
                            nama = "(tidak ditemukan)"

                        try:
                            komentar = el.find_element(By.CLASS_NAME, "css-cvmev1-unf-heading").text
                        except:
                            komentar = "(komentar tidak ditemukan)"

                        try:
                            rating_el = el.find_element(By.CSS_SELECTOR, '[aria-label^="bintang"]')
                            rating = rating_el.get_attribute("aria-label").split()[-1]
                        except:
                            rating = "(rating tidak ditemukan)"

                        try:
                            waktu = el.find_element(By.CLASS_NAME, "css-vqrjg4-unf-heading").text
                        except:
                            waktu = "(waktu tidak ditemukan)"

                        data_review.append({
                                "Nama": nama,
                                "Rating": rating,
                                "Komentar": komentar,
                                "Waktu": waktu,
                            })
                        collected += 1
                    
                    # Klik tombol berikutnya jika tersedia
                    try:
                        next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Laman berikutnya"]')
                        if next_button.is_enabled():
                            next_button.click()
                            time.sleep(2)
                        else:
                            break
                    except:
                        break

                print(f"terambil: {collected}")

                # Uncheck checkbox setelah selesai mengambil review untuk rating ini
                try:
                    area.click()
                except:
                    pass
            
            try:
                if self.cntCheckEnb == 5:
                    reviews = driver.find_elements(By.CSS_SELECTOR, "article.css-15m2bcr")
                    if reviews:
                        for el in reviews:
                            try:
                                tombol = el.find_element(By.CSS_SELECTOR, "button.css-89c2tx")
                                driver.execute_script("arguments[0].click();", tombol)
                                time.sleep(0.2)
                            except:
                                pass
                            try:
                                nama = el.find_element(By.CLASS_NAME, "name").text
                            except:
                                nama = "(tidak ditemukan)"

                            try:
                                komentar = el.find_element(By.CLASS_NAME, "css-cvmev1-unf-heading").text
                            except:
                                komentar = "(komentar tidak ditemukan)"

                            try:
                                rating_el = el.find_element(By.CSS_SELECTOR, '[aria-label^="bintang"]')
                                rating = rating_el.get_attribute("aria-label").split()[-1]
                            except:
                                rating = "(rating tidak ditemukan)"

                            try:
                                waktu = el.find_element(By.CLASS_NAME, "css-vqrjg4-unf-heading").text
                            except:
                                waktu = "(waktu tidak ditemukan)"

                            data_review.append({
                                    "Nama": nama,
                                    "Rating": rating,
                                    "Komentar": komentar,
                                    "Waktu": waktu,
                                })
                    else:
                        return None
            except:
                print("Tidak ada review yang ditemukan setelah semua rating dicentang.")       
                    
            return data_review
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            return None

        finally:
            driver.quit()
