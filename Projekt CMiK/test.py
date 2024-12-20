import tkinter as tk

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