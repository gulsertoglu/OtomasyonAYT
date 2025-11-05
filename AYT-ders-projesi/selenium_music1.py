from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os




SPOTIFY_URL = "https://www.spotify.com/"

CEREZ_KABUL_XPATH = "//button[contains(text(), 'Kabul ediyorum') or contains(text(), 'Accept') or contains(@title, 'Accept')]"
BEKLEME_SURESI = 10 


try:
    
    driver = webdriver.Chrome()
    
    driver.maximize_window()
    
    print(f" {SPOTIFY_URL} adresine gidiliyor")
    driver.get(SPOTIFY_URL)
    

    
    print("Çerez butonunun yüklenmesi bekleniyor")
    
    
    cerez_butonu = WebDriverWait(driver, BEKLEME_SURESI).until(
        EC.element_to_be_clickable((By.XPATH, CEREZ_KABUL_XPATH))
    )
    
    
    cerez_butonu.click()
    print(" Çerezler başarıyla kabul edildi/kapatıldı.")
    
    
    time.sleep(2) 
    
    
    print("\n Siteye Giriş ve Çerezler tamamlandı.")
    
except Exception as e:
    print("\n HATA OLUŞTU:")
    
    if "TimeoutException" in str(e):
        print("Çerez butonu belirlenen süre içinde bulunamadı.")
    else:
        print(f"Beklenmeyen bir hata oluştu: {e}")

finally:
     time.sleep(5) 
     #driver.quit()
    
try:
    load_dotenv()
    
    KULLANICI_ADI = os.environ.get("SPOTIFY_USERNAME")
    SIFRE = os.environ.get("SPOTIFY_PASSWORD")
    Devam = (By.XPATH, "//*[@id='__next']/main/section/div/div/form/button/span")
    kod_atlama = (By.XPATH, "//*[@id='encore-web-main-content']/div[2]/div/div/div/form/div[2]/section/button")

    GIRIS_LOCATOR = (By.XPATH, "//*[text()='Oturum aç' or text()='Log in']") 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(GIRIS_LOCATOR)).click()
    print(" Giriş Yap butonuna başarıyla tıklandı.")
    
    kullanici_LOCATOR = (By.XPATH, "//*[@id='username']") 
    kullanici_alan_elementi = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(kullanici_LOCATOR) 
    )
    kullanici_alan_elementi.send_keys(KULLANICI_ADI) 
    

    devam_elementi = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(Devam))
    devam_elementi.click()
    kod_atlama_elementi = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(kod_atlama))
    kod_atlama_elementi.click()
    
    sifre_LOCATOR = (By.XPATH, "//*[@id='password']")
    sifre_alan_elementi = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(sifre_LOCATOR) 
    )
    sifre_alan_elementi.send_keys(SIFRE) 
    
    devam_elementi_2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(Devam)) 
    devam_elementi_2.click()

    print("Başarıyla giriş yapıldı.")
    
    time.sleep(2) 
    
    
    
    
except TimeoutException:
    print(" Giriş Yap butonu belirlenen süre içinde bulunamadı. Program durduruluyor.")
    driver.quit()
    
except Exception as e:
    print(f" Giriş yapma işleminde beklenmeyen hata: {e}")
    driver.quit()


SEARCH_BUTTON_LOCATOR = (By.XPATH, "//[type='search']") 
SEARCH_INPUT_LOCATOR = (By.XPATH, "//input[@data-testid='search-input']")

Oynatma_dugmesı_locator = (By.XPATH, "//div[@data-testid='action-bar-row']//button[@data-testid='play-button']")
ilk_sarki_satirini_bulma = (By.XPATH, "//div[@data-testid='tracklist-row'][1]//a")

SARKI_ADI = "Ne Farkeder?"
SANATCI_ADI = "Pickpocket"
satir_LOCATOR = "//div[@data-testid='tracklist-row']"



def tam_eslesen_sarki_xpath(sarki_adi):
    return f"{satir_LOCATOR}//div/a[text()='{SARKI_ADI}']"


try:
    print("\n--- ARAMA VE ÇALMA İŞLEMİ BAŞLADI ---")

    print("Arama butonuna tıklanıyor...")
    
    arama_butonu = WebDriverWait(driver, BEKLEME_SURESI).until(
        EC.element_to_be_clickable(SEARCH_BUTTON_LOCATOR)
    )
    arama_butonu.click()
    print("Arama sayfasına geçildi.")

    time.sleep(1) 
    
    
    print(f" '{SARKI_ADI}' aratılıyor...")
    arama_cubugu = WebDriverWait(driver, BEKLEME_SURESI).until(
        EC.presence_of_element_located(SEARCH_INPUT_LOCATOR)
    )
    arama_cubugu.clear()
    
    arama_cubugu.send_keys(SARKI_ADI + Keys.ENTER)
    print("Arama tamamlandı.")
    
    
    sarki_adi_elementi = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, tam_eslesen_sarki_xpath(SARKI_ADI)))
    )
    print(f" '{SARKI_ADI}' şarkısı arama sonuçlarında bulundu.")

    sarki_satiri = sarki_adi_elementi.find_element(By.XPATH, f"ancestor::{satir_LOCATOR}")
    
   
    oynat_dugmesi = sarki_satiri.find_element(By.XPATH, ".//button[@data-testid='play-button']")
    
    
    print(f"Tam eşleşen '{SARKI_ADI}' şarkısındaki oynat düğmesine tıklanıyor...")
    oynat_dugmesi.click()
    print(f" Şarkı '{SARKI_ADI}' oynatılıyor.")

except TimeoutException:
    print(" HATA: Element belirlenen süre içinde bulunamadı. Lütfen Spotify'daki locator'ları kontrol edin.")
except NoSuchElementException:
    print(" HATA: Element bulunamadı. Muhtemelen XPath'ler (özellikle oynat düğmesi veya satır) güncel değil.")
except Exception as e:
    print(f" Arama/Çalma sırasında beklenmeyen hata oluştu: {e}")

finally:
    time.sleep(3600)
    pass