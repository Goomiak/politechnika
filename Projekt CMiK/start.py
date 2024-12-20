import tkinter as tk
from PIL import Image, ImageTk
from menu import create_menu_window

def start_app():
    start_window.destroy()  
    create_menu_window()



start_window = tk.Tk()
start_window.attributes('-fullscreen', True)  
start_window.title("Start")

img = Image.open('wtie.png').convert("RGBA")
img = img.resize((720, 270), Image.Resampling.LANCZOS)  
img_tk = ImageTk.PhotoImage(img)

image_wtie = tk.Label(start_window, image=img_tk)
image_wtie.image = img_tk
image_wtie.pack(pady=30)

title_label = tk.Label(start_window, text="Aplikacja dydaktyczna: zasady detekcji bezpośredniej i koherentnej", font=("Arial", 16), wraplength=1000, justify="center")
title_label.pack(pady=20)

info_label = tk.Label(start_window, text="Aplikacja została wykonana w ramach projektu z przedmiotu Cyfrowe Modulacje i Kodowanie na studiach magisterskich  Kierunek: Elektronika i Telekomunikacja", font=("Arial", 14),  wraplength=1000, justify="center")
info_label.pack(pady=10)

authors_label = tk.Label(start_window, text="Autorzy:\nKamil Jankowski\nFilip Grządziel", font=("Arial", 14))
authors_label.pack(pady=10)

authors_label = tk.Label(start_window, text="Aby rozpocząć wciśnij Start, aby przerwać naciśnij Zamknij", font=("Arial", 14))
authors_label.pack(pady=10)

button_frame = tk.Frame(start_window)
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="Start", font=("Arial", 16), command=start_app)
start_button.pack(side="left", padx=10)

close_button = tk.Button(button_frame, text="Zamknij", font=("Arial", 16), command=start_window.destroy)
close_button.pack(side="left", padx=10)



start_window.mainloop()

