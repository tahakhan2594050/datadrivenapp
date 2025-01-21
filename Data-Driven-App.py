import tkinter as tk
from tkinter import messagebox
from tkinter import font
import requests
from PIL import Image, ImageTk
import io
import webbrowser

# API Key and Base URL
API_KEY = "0ff692aecd23644488f22fa3046f2f8d"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


class StartPage:
    def __init__(self, root, on_start, on_instructions):
        self.root = root
        self.on_start = on_start
        self.on_instructions = on_instructions
        self.create_widgets()

    def create_widgets(self):
        self.bg_image = tk.PhotoImage(file="C://Users//USER//Desktop//image//movie.png")
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        title_frame = tk.Frame(self.root, bg="#101314", bd=0)
        title_frame.place(relx=0.5, rely=0.4, anchor="center")

        title_my_label = tk.Label(
            title_frame,
            text="My",
            font=("Impact", 60, "bold"),
            bg="#000000",
            fg="#fffffa"
        )
        title_my_label.pack(side=tk.LEFT)

        title_prime_label = tk.Label(
            title_frame,
            text="Prime",
            font=("Impact", 60, "bold"),
            bg="#000000",
            fg="#36454f"
        )
        title_prime_label.pack(side=tk.LEFT)

        button_frame = tk.Frame(self.root, bg="#000000")
        button_frame.place(relx=0.5, rely=0.6, anchor="center")

        start_button = tk.Button(
            button_frame,
            text="Start",
            command=self.start_app,
            font=("Century Gothic", 20, "bold"),
            bg="#446a96",
            fg="#fffffa",
            relief=tk.FLAT,
            width=10,
            height=1
        )
        start_button.pack(side=tk.LEFT, padx=10)

        instructions_button = tk.Button(
            button_frame,
            text="Instructions",
            command=self.on_instructions,
            font=("Century Gothic", 20, "bold"),
            bg="#446a96",
            fg="#fffffa",
            relief=tk.FLAT,
            width=12,
            height=1
        )
        instructions_button.pack(side=tk.LEFT, padx=10)

        footer_label = tk.Label(
            self.root,
            text="Created by: Taha Khan",
            font=("Century Gothic", 12),
            bg="#000000",
            fg="#36454f"
        )
        footer_label.place(relx=0.5, rely=0.95, anchor="center")

    def start_app(self):
        self.bg_label.destroy()
        self.on_start()


class InstructionsPage:
    def __init__(self, root, on_back):
        self.root = root
        self.on_back = on_back
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg="#000000")
        self.frame.place(relwidth=1, relheight=1)

        title_label = tk.Label(
            self.frame,
            text="How to Use MyPrime",
            font=("Impact", 30, "bold"),
            bg="#000000",
            fg="#fffffa"
        )
        title_label.pack(pady=20)

        instructions_text = (
            "1. Click 'Start' to browse movies.\n"
            "2. Use the navigation bar to view 'Popular', 'Now Playing', and 'Top Rated' movies.\n"
            "3. Enter a movie name in the search bar and click the search button to find specific movies.\n"
            "4. Click the left or right arrows to navigate between movies.\n"
            "5. Enjoy exploring and discovering new movies!"
        )

        instructions_label = tk.Label(
            self.frame,
            text=instructions_text,
            font=("Century Gothic", 14),
            bg="#000000",
            fg="#fffffa",
            justify=tk.LEFT
        )
        instructions_label.pack(pady=10, padx=20, anchor="w")

        back_button = tk.Button(
            self.frame,
            text="Back",
            command=self.back,
            font=("Century Gothic", 16, "bold"),
            bg="#446a96",
            fg="#fffffa",
            relief=tk.FLAT,
            width=10,
            height=1
        )
        back_button.pack(pady=20)

    def back(self):
        self.frame.destroy()
        self.on_back()


class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MyPrime")
        self.root.geometry("1100x700")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)
        self.show_start_page()

        # Center the window
        self.root.eval('tk::PlaceWindow . center')

        # Fonts
        self.title_font = font.Font(family="Impact", size=24, weight="bold")
        self.label_font = font.Font(family="Century Gothic", size=14)
        self.details_font = font.Font(family="Century Gothic", size=12, weight="bold")
        self.rating_font = font.Font(family="Georgia", size=14, weight="bold")

        # Initialize variables
        self.movies = []
        self.current_index = 0
        self.current_page = 1
        self.total_pages = 1

    def show_start_page(self):
        self.clear_widgets()
        StartPage(self.root, self.create_widgets, self.show_instructions_page)

    def show_instructions_page(self):
        self.clear_widgets()
        InstructionsPage(self.root, self.show_start_page)
    
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):
        self.clear_widgets()
        # Movie browsing UI implementation goes here (not shown for brevity)
        pass

        # Title Label
        title_frame = tk.Frame(self.root, bg="#000000")
        title_frame.pack(pady=10, anchor="w", padx=20)

        title_my_label = tk.Label(
            title_frame, text="My", font=self.title_font, bg="#000000", fg="#fffffa"
        )
        title_my_label.pack(side=tk.LEFT)

        title_prime_label = tk.Label(
            title_frame, text="Prime", font=self.title_font, bg="#000000", fg="#36454f"
        )
        title_prime_label.pack(side=tk.LEFT)

        # Navigation Bar for categories: Popular, Now Playing, Top Rated
        nav_bar = tk.Frame(self.root, bg="#000000")
        nav_bar.pack(pady=10)

        self.popular_button = tk.Button(
            nav_bar,
            text="Popular",
            command=lambda: self.fetch_movies("popular"),
            font=self.label_font,
            bg="#000000",
            fg="#fffffa",
            relief=tk.FLAT,
        )
        self.popular_button.pack(side=tk.LEFT, padx=20)

        self.now_playing_button = tk.Button(
            nav_bar,
            text="Now Playing",
            command=lambda: self.fetch_movies("now_playing"),
            font=self.label_font,
            bg="#000000",
            fg="#fffffa",
            relief=tk.FLAT,
        )
        self.now_playing_button.pack(side=tk.LEFT, padx=20)

        self.top_rated_button = tk.Button(
            nav_bar,
            text="Top Rated",
            command=lambda: self.fetch_movies("top_rated"),
            font=self.label_font,
            bg="#000000",
            fg="#fffffa",
            relief=tk.FLAT,
        )
        self.top_rated_button.pack(side=tk.LEFT, padx=20)

        # Search Bar
        search_frame = tk.Frame(self.root, bg="#000000")
        search_frame.pack(pady=10)

        self.search_entry = tk.Entry(
            search_frame, 
            width=40, 
            font=self.label_font, 
            bg="black",  # Set background to black
            fg="white",  # Set text color to white for contrast
            insertbackground="white",  # Cursor color set to white
            bd=2,  # Border width
            relief="solid",  # Border style
            highlightthickness=1,  # Outline thickness
            highlightcolor="white",  # Outline color white
            highlightbackground="white"  # Border color
        )
        self.search_entry.pack(side=tk.LEFT, padx=5, ipady=5)

        search_button = tk.Button(
            search_frame,
            text="🔍",
            command=self.search_movie,
            font=self.label_font,
            bg="#fffffa",
            fg="black",
            relief=tk.FLAT,
        )
        search_button.pack(side=tk.LEFT, padx=5)

        # Movie Details Frame
        self.details_frame = tk.Frame(self.root, bg="#000000")
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Shadow effect for the image (left and down only)
        self.shadow_label = tk.Label(self.details_frame, bg="#36454f")
        self.shadow_label.place(x=60, y=60, width=200, height=300)

        # Movie Poster
        self.poster_label = tk.Label(self.details_frame, bg="#000000")
        self.poster_label.place(x=50, y=50, width=200, height=300)

        # Description and Details
        info_frame = tk.Frame(self.details_frame, bg="#000000")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(270, 20))

        self.movie_id_label = tk.Label(
            info_frame, text="", font=self.label_font, bg="#000000", fg="#36454f"
        )
        self.movie_id_label.pack(pady=5, anchor="w")

        self.movie_title = tk.Label(
            info_frame, text="", font=("Century Gothic", 14, "bold"), bg="#101314", fg="#fffffa"
        )
        self.movie_title.pack(pady=5, anchor="w")

        self.description_label = tk.Label(
            info_frame, text="", font=self.label_font, wraplength=500, bg="#000000", fg="#fffffa", justify=tk.LEFT
        )
        self.description_label.pack(pady=10, anchor="w")

        self.language_label = tk.Label(
            info_frame, text="", font=self.details_font, bg="#000000", fg="#36454f"
        )
        self.language_label.pack(pady=(5, 0), anchor="w")

        self.rating_label = tk.Label(
            info_frame, text="", font=self.rating_font, bg="#000000", fg="#36454f"
        )
        self.rating_label.pack(pady=(5, 0), anchor="w")

        # Navigation Buttons
        nav_frame = tk.Frame(self.root, bg="#000000")
        nav_frame.pack(pady=10)

        self.prev_button = tk.Button(
            nav_frame,
            text="◀",
            command=self.show_prev_movie,
            font=self.label_font,
            bg="#fffffa",
            fg="black",
            relief=tk.GROOVE,
            borderwidth=2,
        )
        self.prev_button.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        self.page_label = tk.Label(
            nav_frame,
            text="1",
            font=self.label_font,
            bg="#000000",
            fg="#fffffa",
        )
        self.page_label.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(
            nav_frame,
            text="▶",
            command=self.show_next_movie,
            font=self.label_font,
            bg="#fffffa",
            fg="black",
            relief=tk.GROOVE,
            borderwidth=2,
        )
        self.next_button.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

    def fetch_movies(self, category):
        """Fetch movies based on category (Popular, Now Playing, Top Rated)"""
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "page": self.current_page,
        }

        url = f"{BASE_URL}/movie/{category}"

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                self.movies = data.get("results", [])
                self.total_pages = data.get("total_pages", 1)
                self.current_index = 0
                self.show_movie()
            else:
                messagebox.showerror("API Error", "Failed to fetch data from the API.")
        except Exception as e:
            messagebox.showerror("Request Error", f"An error occurred: {str(e)}")

    def search_movie(self):
        query = self.search_entry.get()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a movie name to search.")
            return

        params = {
            "api_key": API_KEY,
            "query": query,
            "language": "en-US",
            "page": 1,
        }

        response = requests.get(f"{BASE_URL}/search/movie", params=params)
        if response.status_code == 200:
            data = response.json()
            self.movies = data.get("results", [])
            if not self.movies:
                messagebox.showinfo("No Results", "No movies found for the given query.")
            else:
                self.current_index = 0
                self.show_movie()
        else:
            messagebox.showerror("API Error", "Failed to fetch data from the API.")

    def show_movie(self):
        if not self.movies:
            return

        movie = self.movies[self.current_index]
        self.movie_id_label.config(text=f"ID: {movie.get('id', 'N/A')}")
        self.movie_title.config(text=movie.get("title", "N/A"))
        poster_path = movie.get("poster_path")
        if poster_path:
            image_url = IMAGE_BASE_URL + poster_path
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                image = image.resize((200, 300))
                photo = ImageTk.PhotoImage(image)
                self.poster_label.config(image=photo)
                self.poster_label.image = photo
            else:
                self.poster_label.config(image="", text="No Image", fg="#36454f")
        else:
            self.poster_label.config(image="", text="No Image", fg="#36454f")

        description = movie.get("overview", "No description available.")
        self.description_label.config(text=description)
        self.language_label.config(text=f"Language: {movie.get('original_language', 'N/A').upper()}")
        self.rating_label.config(text=f"Rating: ★ {movie.get('vote_average', 'N/A')}")
        self.page_label.config(text=f"{self.current_index + 1}")

    def show_next_movie(self):
        if self.current_index < len(self.movies) - 1:
            self.current_index += 1
            self.show_movie()
        else:
            messagebox.showinfo("End of Results", "No more movies to display.")

    def show_prev_movie(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_movie()
        else:
            messagebox.showinfo("Start of Results", "You are already at the first result.")

    def run(self):
        self.show_start_page()




# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    app.run()
    root.mainloop()

