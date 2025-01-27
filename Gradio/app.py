import gradio as gr
import json
from PIL import Image
import random

# Wczytanie konfiguracji
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open("test.json", "r", encoding="utf-8") as f:
    test_data = json.load(f)

def show_start():
    """Wyświetla ekran startowy aplikacji."""
    return "Witaj w aplikacji dydaktycznej! Wybierz jedną z dostępnych opcji, aby kontynuować."

def load_module(module_name):
    """Ładuje i wyświetla moduł dydaktyczny."""
    slides = config['slides'].get(module_name, [])
    module_content = ""
    for slide in slides:
        for element in slide['elements']:
            if element['type'] == 'text':
                module_content += element['content'] + "\n\n"
            elif element['type'] == 'image':
                module_content += f"[Obraz: {element['content']}]\n\n"
    return module_content

def quiz(name):
    """Rozpoczyna test wiedzy."""
    if not name.strip():
        return "Proszę podać imię i nazwisko, aby rozpocząć test!"

    questions = random.sample(test_data['questions'], k=5)
    score = 0

    def evaluate_question(index, answer):
        nonlocal score
        if questions[index]['answer'] == answer:
            score += 1
        if index + 1 == len(questions):
            return f"Test zakończony! Twój wynik: {score}/{len(questions)}"
        return gr.update(visible=True, value=questions[index + 1]['question']), gr.update(visible=True)

    return gr.Interface(
        lambda idx, ans: evaluate_question(idx, ans),
        ["number", "text"],
        ["text", "text"]
    )

# Interfejs główny aplikacji
def app_interface():
    with gr.Blocks() as app:
        gr.Markdown("""# Aplikacja dydaktyczna: Zasady detekcji
        Wybierz odpowiednią zakładkę, aby przejść dalej.
        """)

        with gr.Tab("Start"):
            start_message = gr.Textbox(value=show_start(), interactive=False, label="Ekran startowy")

        with gr.Tab("Moduły"):
            module_choice = gr.Dropdown(
                choices=list(config['slides'].keys()),
                label="Wybierz moduł",
                interactive=True
            )
            module_output = gr.Textbox(label="Treść modułu", interactive=False)
            module_choice.change(load_module, inputs=module_choice, outputs=module_output)

        with gr.Tab("Test wiedzy"):
            name_input = gr.Textbox(label="Imię i nazwisko", placeholder="Wprowadź swoje imię i nazwisko")
            test_output = gr.Textbox(label="Wynik testu", interactive=False)
            start_quiz = gr.Button("Rozpocznij test")
            start_quiz.click(quiz, inputs=name_input, outputs=test_output)

    return app

app_interface.launch(share=True)

if __name__ == "__main__":
    app_interface().launch()