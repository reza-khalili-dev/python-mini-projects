import ttkbootstrap as tb
from tkinter import ttk
from scraper import MovieScraper
from PIL import Image, ImageTk
import requests
from io import BytesIO

scraper = MovieScraper()

def search_movies():
    for widget in results_frame.winfo_children():
        widget.destroy()

    title = entry_title.get()
    genre = combo_genre.get()
    year = combo_year.get()
    rating = combo_rating.get()

    movies = scraper.search_movies(title, genre, year, rating)

    if not movies:
        ttk.Label(results_frame, text="❌ No results found", font=("Arial", 14)).pack(pady=10)
        return

    for movie in movies:
        frame = ttk.Frame(results_frame, padding=5, style="Card.TFrame")
        frame.pack(fill="x", pady=5, padx=5)

        # عکس فیلم
        try:
            resp = requests.get(movie["poster"])
            img = Image.open(BytesIO(resp.content)).resize((100, 150))
            photo = ImageTk.PhotoImage(img)
            lbl_img = ttk.Label(frame, image=photo)
            lbl_img.image = photo
            lbl_img.pack(side="left", padx=5)
        except:
            pass

        info_text = f"{movie['title']} ({movie['year']})\n{movie['genre']}\nRating: {movie['rating']}"
        lbl_info = ttk.Label(frame, text=info_text, justify="left", font=("Arial", 11))
        lbl_info.pack(side="left", padx=10)


        def open_movie(m=movie):
            scraper.open_in_browser(m)

        frame.bind("<Button-1>", lambda e, m=movie: open_movie(m))
        lbl_info.bind("<Button-1>", lambda e, m=movie: open_movie(m))
        if 'lbl_img' in locals():
            lbl_img.bind("<Button-1>", lambda e, m=movie: open_movie(m))



app = tb.Window(themename="superhero")
app.title("Movie Scraper")
app.geometry("1000x700")


ttk.Label(app, text="Title:").pack(pady=2)
entry_title = ttk.Entry(app, width=40)
entry_title.pack(pady=2)


ttk.Label(app, text="Genre:").pack(pady=2)
genres = ["", "Action", "Drama", "Comedy", "Horror", "Sci-Fi", "Thriller", "Romance",
          "Adventure", "Animation", "Crime"]
combo_genre = ttk.Combobox(app, values=genres, width=30)
combo_genre.pack(pady=2)


ttk.Label(app, text="Year:").pack(pady=2)
years = [""] + [str(y) for y in range(1960, 2030)]
combo_year = ttk.Combobox(app, values=years, width=30)
combo_year.pack(pady=2)


ttk.Label(app, text="IMDB Rating Above:").pack(pady=2)
ratings = ["", "5", "6", "7", "8", "9"]
combo_rating = ttk.Combobox(app, values=ratings, width=30)
combo_rating.pack(pady=2)


btn_search = tb.Button(app, text="Search Movies", bootstyle="primary", command=search_movies)
btn_search.pack(pady=10)


results_frame = ttk.Frame(app)
results_frame.pack(fill="both", expand=True)

app.mainloop()
