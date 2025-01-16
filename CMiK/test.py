import json
import tkinter as tk
from datetime import datetime
import random  # Importujemy moduł random

def start_test_window():
    # Funkcja do zapisywania wyników do pliku
    def save_results():
        """Zapisuje wynik testu do pliku."""
        result = f"Imię i nazwisko: {student_name.get()}\n"
        result += f"Data i czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"Wynik: {score['correct']} z {score['total']}\n\n"

        with open("wyniki_testu.txt", "a", encoding="utf-8") as file:
            file.write(result)

    # Funkcja do wyświetlania pytania
    def show_question():
        nonlocal question_index
        if question_index >= len(questions):
            tk.Label(
                test_window,
                text=f"Twój wynik: {score['correct']} z {score['total']}",
                font=("Helvetica", 16),
                bg="white"
            ).pack(pady=20)
            save_results()
            tk.Button(
                test_window,
                text="Zamknij",
                font=("Helvetica", 14),
                command=test_window.destroy
            ).pack(pady=20)
            return

        question = questions[question_index]
        tk.Label(
            test_window,
            text=question.get("question", ""),
            font=("Helvetica", 16),
            wraplength=700,
            bg="white"
        ).pack(pady=10)

        if "image" in question:
            img_path = question["image"]
            try:
                img = tk.PhotoImage(file=img_path)
                img_label = tk.Label(test_window, image=img, bg="white")
                img_label.image = img  # Zachowanie referencji do obrazu
                img_label.pack(pady=10)
            except Exception as e:
                print(f"[ERROR] Nie udało się załadować obrazu {img_path}: {e}")

        for opt, text in question["options"].items():
            tk.Button(
                test_window,
                text=f"{opt}: {text}",
                font=("Helvetica", 14),
                command=lambda opt=opt: answer_question(opt)
            ).pack(pady=5)

    # Funkcja do obsługi odpowiedzi
    def answer_question(selected_option):
        nonlocal question_index
        if questions[question_index]["answer"] == selected_option:
            score["correct"] += 1
        question_index += 1

        for widget in test_window.winfo_children():
            widget.destroy()
        show_question()

    # Okno testowe
    test_window = tk.Toplevel(bg="white")
    test_window.title("Test wiedzy")

    # Wymiary okna
    window_width = 1000
    window_height = 800

    screen_width = test_window.winfo_screenwidth()
    screen_height = test_window.winfo_screenheight()

    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    test_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Wczytanie pytań z pliku JSON
    with open("json/test.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # Losowanie 10 unikalnych pytań
    all_questions = test_data["questions"]
    questions = random.sample(all_questions, 10)  # Wybieramy 10 losowych pytań

    score = {"correct": 0, "total": len(questions)}
    question_index = 0

    # Pole do wprowadzenia imienia i nazwiska
    student_name = tk.StringVar()

    def start_test():
        if not student_name.get().strip():
            tk.Label(
                test_window,
                text="Proszę podać imię i nazwisko!",
                font=("Helvetica", 12),
                fg="red",
                bg="white"
            ).pack(pady=5)
            return

        for widget in test_window.winfo_children():
            widget.destroy()
        show_question()

    tk.Label(
        test_window,
        text="Podaj swoje imię i nazwisko:",
        font=("Helvetica", 16),
        bg="white"
    ).pack(pady=10)

    tk.Entry(
        test_window,
        textvariable=student_name,
        font=("Helvetica", 14),
        width=30
    ).pack(pady=10)

    tk.Button(
        test_window,
        text="Rozpocznij test",
        font=("Helvetica", 14),
        command=start_test
    ).pack(pady=20)