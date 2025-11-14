from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import webbrowser

class MovieScraper:
    def __init__(self):
        options = Options()

        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)
        self.latest_results = []

    def search_movies(self, title="", genre="", year="", rating=""):
        self.latest_results = []

        url = "https://www.imdb.com/search/title/?title_type=feature"

        if title:
            url += f"&title={title}"
        if genre:
            url += f"&genres={genre.lower()}"
        if year:
            url += f"&release_date={year}-01-01,{year}-12-31"
        if rating:
            url += f"&user_rating={rating},10"

        self.driver.get(url)
        time.sleep(2)

        movies = []
        items = self.driver.find_elements(By.CSS_SELECTOR, ".lister-item")
        for item in items[:20]: 
            try:
                title_elem = item.find_element(By.CSS_SELECTOR, ".lister-item-header a")
                title_text = title_elem.text
                link = title_elem.get_attribute("href")
                year_text = item.find_element(By.CSS_SELECTOR, ".lister-item-year").text
                genre_text = item.find_element(By.CSS_SELECTOR, ".genre").text.strip()
                rating_text = item.find_element(By.CSS_SELECTOR, ".ratings-imdb-rating strong").text
                poster = item.find_element(By.CSS_SELECTOR, ".lister-item-image img").get_attribute("src")

                movie_data = {
                    "title": title_text,
                    "year": year_text,
                    "genre": genre_text,
                    "rating": rating_text,
                    "poster": poster,
                    "link": link
                }
                movies.append(movie_data)
            except:
                pass

        self.latest_results = movies
        return movies

    def open_in_browser(self, movie):
        webbrowser.open(movie["link"])
