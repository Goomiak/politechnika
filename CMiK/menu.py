import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from slides import show_window_sequence, load_config
import subprocess
from test import start_test_window

def create_menu_window():
    menu_window = tk.Tk()
    menu_window.attributes('-fullscreen', True)  # Pełny ekran
    menu_window.title("Choose Detection Method")

    # Wczytaj konfigurację
    config = load_config("config.json")

    # Śledzenie stanu obejrzanych slajdów
    viewed_slides = {"direct_detection": False, "coherent_detection": False, "summary": False}

    # Funkcje do obsługi kliknięć na ikony
    def on_direct_detection():
        slides = config["slides"]["direct_detection"]
        show_window_sequence(slides, "Direct Detection")
        viewed_slides["direct_detection"] = True
        update_test_button_state()

    def on_coherent_detection():
        slides = config["slides"]["coherent_detection"]
        show_window_sequence(slides, "Coherent Detection")
        viewed_slides["coherent_detection"] = True
        update_test_button_state()

    def on_summary():
        slides = config["slides"]["summary"]
        show_window_sequence(slides, "Summary")
        viewed_slides["summary"] = True
        update_test_button_state()

    def update_test_button_state():
        # Jeśli wszystkie moduły zostały obejrzane, aktywuj przycisk testu
        if all(viewed_slides.values()):
            test_button.config(state="normal")

    def start_test():
        try:
            start_test_window()
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się uruchomić testu: {e}")

    # Nagłówki i opisy
    title_label = tk.Label(
        menu_window,
        text=("Kliknij ikonę i wybierz zagadnienie, które chcesz trenować: "
              "Detekcja Bezpośrednia / Detekcja Koherentna / Podsumowanie."),
        font=("Arial", 16), wraplength=1000, justify="center"
    )
    title_label.pack(pady=20)

    info_label = tk.Label(
        menu_window,
        text=("Każdy z modułów zawiera wstęp teoretyczny, animacje, "
              "model matematyczny oraz symulację interaktywną."),
        font=("Arial", 16), wraplength=1000, justify="center"
    )
    info_label.pack(pady=20)

    # Wczytywanie obrazów
    icon1 = Image.open("1-png.png").resize((300, 300), Image.Resampling.LANCZOS)
    icon1_tk = ImageTk.PhotoImage(icon1)

    icon2 = Image.open("2-png.png").resize((300, 300), Image.Resampling.LANCZOS)
    icon2_tk = ImageTk.PhotoImage(icon2)

    icon3 = Image.open("3-png.png").resize((300, 300), Image.Resampling.LANCZOS)
    icon3_tk = ImageTk.PhotoImage(icon3)

    # Ramka dla przycisków
    button_frame = tk.Frame(menu_window)
    button_frame.pack(pady=20)

    # Ikona "Detekcja bezpośrednia"
    btn_direct = tk.Label(button_frame, image=icon1_tk, cursor="hand2")
    btn_direct.image = icon1_tk  # Zachowanie referencji do obrazu
    btn_direct.bind("<Button-1>", lambda e: on_direct_detection())
    btn_direct.pack(side="left", padx=20)

    # Ikona "Detekcja koherentna"
    btn_coherent = tk.Label(button_frame, image=icon2_tk, cursor="hand2")
    btn_coherent.image = icon2_tk  # Zachowanie referencji do obrazu
    btn_coherent.bind("<Button-1>", lambda e: on_coherent_detection())
    btn_coherent.pack(side="left", padx=20)

    # Ikona "Podsumowanie"
    btn_summary = tk.Label(button_frame, image=icon3_tk, cursor="hand2")
    btn_summary.image = icon3_tk  # Zachowanie referencji do obrazu
    btn_summary.bind("<Button-1>", lambda e: on_summary())
    btn_summary.pack(side="left", padx=20)

    info_label = tk.Label(
        menu_window,
        text=("Przycisk stanie się aktywny po obejrzeniu wszystkich modułów."
              " ."),
        font=("Arial", 16), wraplength=1000, justify="center"
    )
    info_label.pack(pady=20)

    # Przycisk "Test wiedzy"
    test_button = tk.Button(
        menu_window,
        text="Test wiedzy",
        font=("Arial", 16),
        state="disabled",
        command=start_test
    )
    test_button.pack(pady=20)

    # Przycisk "Close" dla okna menu
    close_button = tk.Button(menu_window, text="Zamknij", font=("Arial", 16), command=menu_window.destroy)
    close_button.pack(pady=10)

    menu_window.mainloop()
