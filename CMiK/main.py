import tkinter as tk
from slides import show_window_sequence
from menu import create_menu_window
from PIL import Image, ImageTk

def start_app():
    start_window.destroy()  # Zamknięcie okna startowego
    create_menu_window()

# Tworzenie okna startowego
start_window = tk.Tk()
start_window.attributes('-fullscreen', True)  # Pełny ekran
start_window.title("Start")

# Nagłówek
img = Image.open('wtie.png').resize((720, 270), Image.Resampling.LANCZOS)
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
