
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# driver auto install
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.digikala.com/search/category-mobile-phone/?categoryCode=category-mobile-phone")
#driver.get("https://www.digikala.com/product/dkp-20519415/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%86%D8%A7%D8%AA%DB%8C%D9%86%DA%AF-%D9%85%D8%AF%D9%84-cmf-phone-1-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/e")
html_code = driver.page_source

time.sleep(30)  # wait for loading

html_code = driver.page_source
print(html_code)
driver.quit()