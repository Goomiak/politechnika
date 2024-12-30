import json
import tkinter as tk

def start_test_window():
    test_window = tk.Toplevel(bg="white")
    test_window.title("Test wiedzy")
    test_window.geometry("800x600")

    with open("test.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    questions = test_data["questions"]

    score = {"correct": 0, "total": len(questions)}
    question_index = 0

    def show_question():
        nonlocal question_index
        if question_index >= len(questions):
            tk.Label(test_window, text=f"Twój wynik: {score['correct']} z {score['total']}", font=("Helvetica", 16), bg="white").pack(pady=20)
            return

        question = questions[question_index]
        tk.Label(test_window, text=question["question"], font=("Helvetica", 16), wraplength=700, bg="white").pack(pady=10)

        for opt, text in question["options"].items():
            tk.Button(test_window, text=f"{opt}: {text}", font=("Helvetica", 14),
                      command=lambda opt=opt: answer_question(opt)).pack(pady=5)

    def answer_question(selected_option):
        nonlocal question_index
        if questions[question_index]["answer"] == selected_option:
            score["correct"] += 1
        question_index += 1

        for widget in test_window.winfo_children():
            widget.destroy()
        show_question()

    show_question()
