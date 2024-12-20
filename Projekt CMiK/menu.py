import tkinter as tk
from PIL import Image, ImageTk
from slides import show_direct_detection, show_coherent_detection
from test import show_final_test
from helpers import are_all_slides_viewed

def create_menu_window():
    menu_window = tk.Tk()
    menu_window.attributes('-fullscreen', True)
    menu_window.title("Choose Detection Method")

    icon1 = Image.open("1-png.png").resize((300, 300), Image.Resampling.LANCZOS)
    icon1_tk = ImageTk.PhotoImage(icon1)

    icon2 = Image.open("2-png.png").resize((300, 300), Image.Resampling.LANCZOS)
    icon2_tk = ImageTk.PhotoImage(icon2)

    icon3 = Image.open("3-png.png").resize((300, 300), Image.Resampling.LANCZOS)
    icon3_tk = ImageTk.PhotoImage(icon3)

    def update_final_button():
        if are_all_slides_viewed():
            btn_final.config(state=tk.NORMAL)

    def on_direct_detection():
        show_direct_detection(menu_window, update_final_button)

    def on_coherent_detection():
        show_coherent_detection(menu_window, update_final_button)

    title_label = tk.Label(
        menu_window,
        text="Kliknij ikonę i wybierz zagadnienie, które chcesz trenować: Detekcja Bezpośrednia / Detekcja Koherentna.",
        font=("Arial", 16),
        wraplength=1000,
        justify="center"
    )
    title_label.pack(pady=20)

    info_label = tk.Label(
        menu_window,
        text="Każdy z modułów zawiera wstęp teoretyczny, animacje, model matematyczny oraz symulację interaktywną.",
        font=("Arial", 16),
        wraplength=1000,
        justify="center"
    )
    info_label.pack(pady=20)

    button_frame = tk.Frame(menu_window)
    button_frame.pack(pady=20)

    btn_direct = tk.Label(button_frame, image=icon1_tk, cursor="hand2")
    btn_direct.image = icon1_tk
    btn_direct.bind("<Button-1>", lambda e: on_direct_detection())
    btn_direct.pack(side="left", padx=20)

    btn_coherent = tk.Label(button_frame, image=icon2_tk, cursor="hand2")
    btn_coherent.image = icon2_tk
    btn_coherent.bind("<Button-1>", lambda e: on_coherent_detection())
    btn_coherent.pack(side="left", padx=20)

    btn_summary = tk.Label(button_frame, image=icon3_tk, cursor="hand2")
    btn_summary.image = icon3_tk
    btn_summary.bind("<Button-1>", lambda e: None)
    btn_summary.pack(side="left", padx=20)

    test_label = tk.Label(
        menu_window,
        text="Po ukończeniu wszystkich modułów, aktywuje się poniższy przycisk.\n Odpowiedz na 15 pytań i sprawdź swoją wiedzę.",
        font=("Arial", 16),
        wraplength=1000,
        justify="center"
    )
    test_label.pack(pady=20)

    btn_final = tk.Button(
        menu_window,
        text="Test wiedzy",
        state=tk.DISABLED,
        font=("Arial", 16),
        command=show_final_test
    )
    btn_final.pack(pady=10)

    close_button = tk.Button(menu_window, text="Zamknij", font=("Arial", 16), command=menu_window.destroy)
    close_button.pack(pady=10)

    menu_window.mainloop()
