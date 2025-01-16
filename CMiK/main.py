import tkinter as tk
from slides import show_window_sequence
from menu import create_menu_window
from PIL import Image, ImageTk
import math

def calculate_screen_diagonal(width, height):
    """Oblicza przekątną ekranu w calach."""
    diagonal = math.sqrt(width ** 2 + height ** 2)
    return diagonal / 96  # Zakładamy 96 DPI (pikseli na cal)

def configure_window(window, title="Start"):
    """Konfiguruje okno w zależności od wielkości ekranu."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Oblicz przekątną ekranu w calach
    diagonal_inches = calculate_screen_diagonal(screen_width, screen_height)

    if diagonal_inches <= 19:  # Dla ekranów 19 cali i mniejszych pełny ekran
        window.attributes('-fullscreen', True)
    else:  # Dla większych ekranów ustaw rozmiar okna na środku
        window_width = 1300
        window_height = 800
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    window.title(title)

def start_app():
    start_window.destroy()  # Zamknięcie okna startowego
    create_menu_window()

# Tworzenie okna startowego
start_window = tk.Tk()
configure_window(start_window)

# Nagłówek
img = Image.open('img/wtie.png').resize((720, 270), Image.Resampling.LANCZOS)
img_tk = ImageTk.PhotoImage(img)
image_wtie = tk.Label(start_window, image=img_tk)
image_wtie.image = img_tk
image_wtie.pack(pady=30)

title_label = tk.Label(
    start_window, 
    text="Aplikacja dydaktyczna: zasady detekcji bezpośredniej i koherentnej",
    font=("Arial", 16), wraplength=1000, justify="center"
)
title_label.pack(pady=20)

info_label = tk.Label(
    start_window, 
    text=(
        "Aplikacja została wykonana w ramach projektu z przedmiotu Cyfrowe Modulacje i Kodowanie na studiach magisterskich "
        "Kierunek: Elektronika i Telekomunikacja"
    ), 
    font=("Arial", 14), wraplength=1000, justify="center"
)
info_label.pack(pady=10)

authors_label = tk.Label(
    start_window, 
    text="Autorzy:\nKamil Jankowski\nFilip Grządziel",
    font=("Arial", 14)
)
authors_label.pack(pady=10)

authors_label = tk.Label(
    start_window, 
    text="Aby rozpocząć wciśnij Start, aby przerwać naciśnij Zamknij",
    font=("Arial", 14)
)
authors_label.pack(pady=10)

button_frame = tk.Frame(start_window)
button_frame.pack(pady=20)

# Przycisk "Start"
start_button = tk.Button(button_frame, text="Start", font=("Arial", 16), command=start_app)
start_button.pack(side="left", padx=10)

# Przycisk "Close"
close_button = tk.Button(button_frame, text="Zamknij", font=("Arial", 16), command=start_window.destroy)
close_button.pack(side="left", padx=10)

start_window.mainloop()
