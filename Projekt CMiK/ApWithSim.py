import tkinter as tk
import textwrap
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

direct_slides_viewed = True
coherent_slides_viewed = True
summary_slides_viewed = False

# Funkcja aktualizująca status przycisku "Final"
def update_final_button(menu_window, final_button):
    if direct_slides_viewed and coherent_slides_viewed:
        final_button.config(state=tk.NORMAL)


# Funkcja startowa - przejście do okna wyboru
def start_app():
    start_window.destroy()  # Zamknięcie okna startowego
    create_menu_window()

# Funkcja zarządzająca slajdami w oknie Direct Detection
def show_direct_detection(menu_window, final_button):
    slides = [
        ("image_text", "direct.png", "Detekcja bezpośrednia", "Detekcja bezpośrednia sygnałów optycznych polega na bezpośrednim pomiarze mocy promieniowania optycznego przy użyciu detektorów, takich jak fotodiody czy fotopowielacze. Proces ten polega na konwersji fotonów padających na detektor na sygnał elektryczny, którego natężenie jest proporcjonalne do mocy optycznej padającego światła."),
        ("simulation", "direct_sim_1", "Interaktywna symulacja detekcji bezpośredniejdddddddd", "sssss"),
        ("simulation", "direct_sim_2", "Interaktywna symulacja detekcji koherentnejdddd", "sssssssss")
    ]

    show_window_sequence(slides, "Direct Detection", lambda: mark_direct_slides_as_viewed(menu_window, final_button))

# Funkcja zarządzająca slajdami w oknie Coherent Detection
def show_coherent_detection(menu_window, final_button):
    slides = [
        ("image_text", "path/to/image1.png", "To jest slajd z tekstem i obrazem."),
        ("simulation", "Detekcja Bezpośrednia", "Interaktywna symulacja detekcji bezpośredniejdddddddd"),
        ("simulation", "Detekcja Koherentna", "Interaktywna symulacja detekcji koherentnejdddd")
    ]
    show_window_sequence(slides, "Coherent Detection", lambda: mark_coherent_slides_as_viewed(menu_window, final_button))

# Funkcja do oznaczania slajdów Direct jako obejrzane
def mark_direct_slides_as_viewed(menu_window, final_button):
    global direct_slides_viewed
    direct_slides_viewed = True
    update_final_button(menu_window, final_button)

# Funkcja do oznaczania slajdów Coherent jako obejrzane
def mark_coherent_slides_as_viewed(menu_window, final_button):
    global coherent_slides_viewed
    coherent_slides_viewed = True
    update_final_button(menu_window, final_button)



# Funkcja tworząca sekwencję okien slajdów
def show_window_sequence(slides, title, on_finish):
    def create_slide_window(index):
        slide_window = tk.Toplevel()
        slide_window.attributes('-fullscreen', True)
        slide_window.title(title)

        slide_type, content, slide_title, slide_text = slides[index]

        # Tytuł slajdu
        title_label = tk.Label(slide_window, text=slide_title, font=("Helvetica", 20, "bold"))
        title_label.pack(pady=(20, 10))

        # Formatowanie i dzielenie tekstu slajdu
        wrapper = textwrap.TextWrapper(width=120)
        word_list = wrapper.wrap(text=slide_text)
        formatted_text = '\n'.join(word_list)

        text_label = tk.Label(slide_window, text=formatted_text, font=("Helvetica", 16), justify="left")
        text_label.pack(pady=10)

        if slide_type == "image_text":
            # Obraz
            image_path = content  # Zakładamy, że content to ścieżka do obrazu
            image = Image.open(image_path)
            image = image.resize((600, 400), Image.Resampling.LANCZOS)  # Dostosowanie rozmiaru obrazu
            img_tk = ImageTk.PhotoImage(image)

            image_label = tk.Label(slide_window, image=img_tk)
            image_label.image = img_tk  # Trzymanie referencji do obrazu
            image_label.pack()
        elif slide_type == "simulation":
            # Wprowadź logikę symulacji bez zamykania okna
            param_frame = tk.Frame(slide_window)
            param_frame.pack(side=tk.TOP, pady=20)

            param_label = tk.Label(param_frame, text="Wprowadź parametry symulacji:", font=("Arial", 16))
            param_label.pack()

            # Parametry symulacji
            param_amplitude = tk.DoubleVar(value=1.0)
            param_frequency = tk.DoubleVar(value=1.0)
            param_noise = tk.DoubleVar(value=0.1)

            

            def plot_simulation():
                amplitude = param_amplitude.get()
                frequency = param_frequency.get()
                noise_level = param_noise.get()

                t = np.linspace(0, 1, 1000)
                signal = amplitude * np.sin(2 * np.pi * frequency * t)
                noise = noise_level * np.random.normal(size=t.shape)

                ax.clear()
                if simulation_type == "Detekcja Koherentna":
                    ax.plot(t, signal + noise, label="Sygnał koherentny")
                else:
                    ax.plot(t, np.abs(signal) + noise, label="Sygnał bezpośredni")
                ax.legend()
                canvas.draw()

            param_amplitude.trace("w", lambda *_: plot_simulation())
            param_frequency.trace("w", lambda *_: plot_simulation())
            param_noise.trace("w", lambda *_: plot_simulation())

            tk.Label(param_frame, text="Amplituda").pack()
            tk.Entry(param_frame, textvariable=param_amplitude).pack()

            tk.Label(param_frame, text="Częstotliwość").pack()
            tk.Entry(param_frame, textvariable=param_frequency).pack()

            tk.Label(param_frame, text="Poziom szumu").pack()
            tk.Entry(param_frame, textvariable=param_noise).pack()

            # Rysowanie wykresu
            figure = plt.Figure(figsize=(10, 5), dpi=100)
            ax = figure.add_subplot(111)
            canvas = FigureCanvasTkAgg(figure, slide_window)
            canvas.get_tk_widget().pack()

            plot_simulation()


        # Pasek nawigacyjny
        nav_frame = tk.Frame(slide_window)
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Funkcje nawigacji
        def next_slide():
            if index < len(slides) - 1:
                create_slide_window(index + 1)
            else:
                on_finish()

        def previous_slide():
            if index > 0:
                create_slide_window(index - 1)

        # Przyciski nawigacyjne
        back_button = tk.Button(nav_frame, text="Wstecz", command=previous_slide)
        back_button.pack(side=tk.LEFT, padx=20, pady=20)
        back_button.config(state=tk.NORMAL if index > 0 else tk.DISABLED)

        next_button = tk.Button(nav_frame, text="Dalej", command=next_slide)
        next_button.pack(side=tk.RIGHT, padx=20, pady=20)
        next_button.config(text="Zakończ" if index == len(slides) - 1 else "Dalej")

    # Uruchomienie pierwszego slajdu
    create_slide_window(0)


# Funkcja wyświetlająca okno z testem
def show_final_test():
    final_window = tk.Toplevel()
    final_window.attributes('-fullscreen', True)
    final_window.title("Test")

    sections = [
        {
            "title": "Detekcja Bezpośrednia",
            "questions": [
                "Pytanie 1: Co to jest detekcja bezpośrednia?",
                "Pytanie 2: Jaki jest podstawowy mechanizm detekcji bezpośredniej?",
                "Pytanie 3: W jakim zakresie używana jest detekcja bezpośrednia?",
                "Pytanie 4: Jakie są zalety detekcji bezpośredniej?",
                "Pytanie 5: Kiedy warto stosować detekcję bezpośrednią?"
            ],
            "answers": [
                ["a) Bezpośrednie przetwarzanie sygnału", "b) Odbiór sygnału z modulacją", "c) Odbiór sygnału z kodowaniem", "d) Użycie tylko jednego detektora"],
                ["a) Analiza częstotliwości", "b) Użycie detektora amplitudy", "c) Użycie detektora fazy", "d) Użycie analizy sygnału"],
                ["a) Tylko w zakresie optycznym", "b) W każdym zakresie częstotliwości", "c) Głównie w zakresie radiowym", "d) Tylko w zakresie mikrofalowym"],
                ["a) Łatwość implementacji", "b) Niskie koszty", "c) Wysoka dokładność", "d) Niska odporność na zakłócenia"],
                ["a) W prostych systemach", "b) W systemach o dużej złożoności", "c) Tylko w komunikacji optycznej", "d) W systemach z niską jakością sygnału"]
            ]
        },
        {
            "title": "Detekcja Koherentna",
            "questions": [
                "Pytanie 6: Co to jest detekcja koherentna?",
                "Pytanie 7: Jaki jest podstawowy mechanizm detekcji koherentnej?",
                "Pytanie 8: Jakie są korzyści stosowania detekcji koherentnej?",
                "Pytanie 9: Jakie są ograniczenia detekcji koherentnej?",
                "Pytanie 10: Kiedy warto stosować detekcję koherentną?"
            ],
            "answers": [
                ["a) Użycie sygnału referencyjnego", "b) Odbiór sygnału w postaci cyfrowej", "c) Bezpośrednia analiza amplitudy", "d) Analiza fazy bez sygnału referencyjnego"],
                ["a) Analiza amplitudy sygnału", "b) Analiza sygnału w czasie", "c) Użycie sygnału odniesienia", "d) Użycie jednego detektora"],
                ["a) Większa odporność na szumy", "b) Wyższa dokładność pomiarów", "c) Możliwość detekcji sygnałów o niskim poziomie", "d) Wszystkie powyższe"],
                ["a) Wymagana synchronizacja", "b) Wysokie koszty implementacji", "c) Wymaga zaawansowanej technologii", "d) Wszystkie powyższe"],
                ["a) W systemach o wysokiej jakości sygnału", "b) W prostych aplikacjach", "c) W komunikacji radiowej", "d) W aplikacjach o niskim poziomie sygnału"]
            ]
        },
        {
            "title": "Różnice",
            "questions": [
                "Pytanie 11: Jaka jest główna różnica między detekcją bezpośrednią a koherentną?",
                "Pytanie 12: Która metoda wymaga dodatkowych zasobów?",
                "Pytanie 13: Która metoda jest bardziej odporna na szumy?",
                "Pytanie 14: Która metoda ma większą precyzję?",
                "Pytanie 15: Która metoda jest częściej stosowana w praktyce?"
            ],
            "answers": [
                ["a) Detekcja koherentna używa sygnału odniesienia", "b) Detekcja bezpośrednia jest zawsze szybsza", "c) Detekcja koherentna nie wymaga analizy fazy", "d) Nie ma między nimi różnicy"],
                ["a) Detekcja koherentna", "b) Detekcja bezpośrednia", "c) Obie metody są równorzędne", "d) Żadna z nich"],
                ["a) Detekcja koherentna", "b) Detekcja bezpośrednia", "c) Obie metody są równorzędne", "d) Żadna z nich"],
                ["a) Detekcja bezpośrednia", "b) Detekcja koherentna", "c) Obie metody mają tę samą precyzję", "d) Żadna z nich"],
                ["a) Detekcja koherentna", "b) Detekcja bezpośrednia", "c) Obie metody są równorzędne", "d) To zależy od aplikacji"]
            ]
        }
    ]

    correct_answers = [
        "a", "b", "c", "a", "a",  
        "a", "c", "d", "d", "a",  
        "a", "a", "a", "b", "d"
    ]

    current_section = 0
    question_labels = []
    answer_vars = []  # Lista na zmienne StringVar

    # Funkcja inicjalizująca `StringVar` dla nowej sekcji
    def initialize_answer_vars():
        nonlocal answer_vars
        answer_vars = [tk.StringVar(value="") for _ in range(5)]  # Resetowanie zmiennych

    # Funkcja aktualizująca zawartość sekcji
    def update_section():
        section = sections[current_section]
        section_label.config(text=section["title"])

        for i in range(5):
            question_labels[i].config(text=section["questions"][i])  # Ustaw pytanie
            question_labels[i].pack(pady=5)

            # Usuwanie poprzednich przycisków
            for widget in answer_frames[i].winfo_children():
                widget.destroy()

            # Tworzenie przycisków opcji odpowiedzi
            for option, answer in zip(['a', 'b', 'c', 'd'], section["answers"][i]):
                radio_button = tk.Radiobutton(
                    answer_frames[i], text=answer, variable=answer_vars[i], value=option
                )
                radio_button.pack(side=tk.LEFT)

    # Nagłówek sekcji
    section_label = tk.Label(final_window, font=("Arial", 20))
    section_label.pack(pady=40)

    question_frames = []
    answer_frames = []

    # Dodanie pytań i opcji odpowiedzi
    for i in range(5):
        question_frame = tk.Frame(final_window)
        question_frame.pack(pady=10)

        question_label = tk.Label(question_frame, font=("Arial", 18))
        question_labels.append(question_label)

        question_label.pack()  # Ustawienie pytania nad opcjami

        answer_frame = tk.Frame(question_frame)
        answer_frames.append(answer_frame)
        answer_frame.pack()

    # Funkcja obsługująca przycisk Next
    def next_section():
        nonlocal current_section
        if current_section < len(sections) - 1:
            current_section += 1
            initialize_answer_vars()  # Nowa instancja `StringVar` dla nowej sekcji
            update_section()
        else:
            show_result()

    # Funkcja wyświetlająca wynik
    def show_result():
        final_window.destroy()
        score = sum(1 for i, answer_var in enumerate(answer_vars) if answer_var.get() == correct_answers[i])

        result_window = tk.Toplevel()
        result_window.title("Wynik")
        result_label = tk.Label(result_window, text=f"Twój wynik: {score}/15", font=("Helvetica", 16))
        result_label.pack(pady=20)
        tk.Button(result_window, text="Zamknij", command=result_window.destroy).pack(pady=20)

    # Przycisk Next
    next_button = tk.Button(final_window, text="Next", font=("Helvetica", 16), command=next_section)
    next_button.pack(pady=20)

    initialize_answer_vars()  # Inicjalizacja `StringVar` dla pierwszej sekcji
    update_section()

# Upewnij się, że reszta kodu aplikacji jest poprawna, a powyższa funkcja zostaje dodana do Twojego programu.

# Tworzenie okna z menu wyboru
def create_menu_window():
    menu_window = tk.Tk()
    menu_window.attributes('-fullscreen', True)  # Pełny ekran
    menu_window.title("Choose Detection Method")

    # Wczytywanie obrazów
    icon1 = Image.open("1-png.png")
    icon1 = icon1.resize((300, 300), Image.Resampling.LANCZOS)  # Dostosowanie rozmiaru obrazu
    icon1_tk = ImageTk.PhotoImage(icon1)

    icon2 = Image.open("2-png.png")
    icon2 = icon2.resize((300, 300), Image.Resampling.LANCZOS)  # Dostosowanie rozmiaru obrazu
    icon2_tk = ImageTk.PhotoImage(icon2)

    icon3 = Image.open("3-png.png")
    icon3 = icon3.resize((300, 300), Image.Resampling.LANCZOS)  # Dostosowanie rozmiaru obrazu
    icon3_tk = ImageTk.PhotoImage(icon3)

    # Funkcje do obsługi kliknięć na ikony
    def on_direct_detection():
        show_direct_detection(menu_window, btn_final)

    def on_coherent_detection():
        show_coherent_detection(menu_window, btn_final)

    def on_summary():
        show_coherent_detection(menu_window, btn_final)

    title_label = tk.Label(menu_window, text="Kliknij ikonę i wybierz zagadnienie, które chcesz trenować: Detekcja Bezpośrednia / Detekcja Koherentna.", font=("Arial", 16), wraplength=1000, justify="center")
    title_label.pack(pady=20)

    info_label = tk.Label(menu_window, text="Każdy z modułów zawiera wstęp teoretyczny, animacje, model matematyczny oraz symulację interaktywną. ", font=("Arial", 16), wraplength=1000, justify="center")
    info_label.pack(pady=20)


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
    btn_coherent = tk.Label(button_frame, image=icon3_tk, cursor="hand2")
    btn_coherent.image = icon3_tk  # Zachowanie referencji do obrazu
    btn_coherent.bind("<Button-1>", lambda e: on_summary())
    btn_coherent.pack(side="left", padx=20)

    test_label = tk.Label(menu_window, text="Po ukończeniu wszystkich modułów, aktywuje się poniższy przycisk.\n Odpowiedz na 15 pytań i sprawdź swoją wiedzę.", font=("Arial", 16), wraplength=1000, justify="center")
    test_label.pack(pady=20)

    # Przycisk "Final" (początkowo nieaktywny)
    btn_final = tk.Button(menu_window, text="Test wiedzy", state=tk.DISABLED, font=("Arial", 16), command=show_final_test)
    btn_final.pack(pady=10)

    # Przycisk "Close" dla okna menu
    close_button = tk.Button(menu_window, text="Zamknij", font=("Arial", 16), command=menu_window.destroy)
    close_button.pack(pady=10)

    menu_window.mainloop()

# Tworzenie okna startowego
start_window = tk.Tk()
start_window.attributes('-fullscreen', True)  # Pełny ekran
start_window.title("Start")

img = Image.open('wtie.png').convert("RGBA")
img = img.resize((720, 270), Image.Resampling.LANCZOS)  # Zmiana rozmiaru obrazka, jeśli potrzebne
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

# Przycisk "Start"
start_button = tk.Button(button_frame, text="Start", font=("Arial", 16), command=start_app)
start_button.pack(side="left", padx=10)

# Przycisk "Close"
close_button = tk.Button(button_frame, text="Zamknij", font=("Arial", 16), command=start_window.destroy)
close_button.pack(side="left", padx=10)




start_window.mainloop()
