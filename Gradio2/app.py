import os
import gradio as gr
import matplotlib.pyplot as plt
import numpy as np

print(os.path.exists("C:/GitHub/politechnika/Gradio2/wtie.png"))
print("Current working directory:", os.getcwd())

print("Current working directory:", os.getcwd())
print("Czy plik istnieje?", os.path.exists("wtie.png"))
print("Pełna ścieżka:", os.path.abspath("wtie.png"))

# Funkcja do generowania przykładowego wykresu
def generate_plot():
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)
    plt.figure(figsize=(5, 3))
    plt.plot(x, y, label="sin(x)")
    plt.title("Przykładowy Wykres")
    plt.legend()
    plt.grid(True)
    plt.savefig("temp_plot.png")
    plt.close()
    return "<img src='temp_plot.png' style='width: 100%; height: auto;'>"


# Moduły
def module_1(step: int):
    slides = [
        ("Slide 1", "Pierwszy slajd w module 1", "<img src='1-png.png' style='width: 100%; height: auto;'>"),
        ("Slide 2", "Drugi slajd w module 1 z wykresem", generate_plot()),
        ("Slide 3", "Trzeci slajd w module 1 z GIF-em", "<img src='example.gif' style='width: 100%; height: auto;'>"),
    ]
    step = step % len(slides)
    return slides[step]


def module_2(step: int):
    slides = [
        ("Slide 1", "Pierwszy slajd w module 2", "<img src='2-png.png' style='width: 100%; height: auto;'>"),
        ("Slide 2", "Drugi slajd w module 2 z wykresem", generate_plot()),
        ("Slide 3", "Trzeci slajd w module 2 z GIF-em", "<img src='example.gif' style='width: 100%; height: auto;'>"),
    ]
    step = step % len(slides)
    return slides[step]


def module_3(step: int):
    slides = [
        ("Slide 1", "Pierwszy slajd w module 3", "<img src='3-png.png' style='width: 100%; height: auto;'>"),
        ("Slide 2", "Drugi slajd w module 3 z wykresem", generate_plot()),
        ("Slide 3", "Trzeci slajd w module 3 z GIF-em", "<img src='example.gif' style='width: 100%; height: auto;'>"),
    ]
    step = step % len(slides)
    return slides[step]


# Budowanie aplikacji
with gr.Blocks() as demo:
    # Ekran główny
    with gr.Row():
        gr.HTML("<img src='wtie.png' style='width: 150px; height: auto;'>")
    gr.Markdown("<h1 style='text-align: center;'>Witaj w aplikacji</h1>")
    gr.Markdown("<p style='text-align: center;'>Kliknij w ikonę, aby przejść do modułu:</p>")
    with gr.Row():
        icon1 = gr.HTML("<a href='#mod1'><img src='1-jpg.jpg' style='width: 100px; height: auto; cursor: pointer;'></a>")
        icon2 = gr.HTML("<a href='#mod2'><img src='2-png.png' style='width: 100px; height: auto; cursor: pointer;'></a>")
        icon3 = gr.HTML("<a href='#mod3'><img src='3-png.png' style='width: 100px; height: auto; cursor: pointer;'></a>")

    # Moduł 1
    with gr.Row(visible=False, elem_id="mod1") as mod1_view:
        title1 = gr.Textbox(label="Tytuł", interactive=False)
        desc1 = gr.Textbox(label="Opis", interactive=False)
        img1 = gr.HTML()
        step1 = gr.Number(value=0, visible=False)
        with gr.Row():
            prev_btn1 = gr.Button("Poprzedni")
            next_btn1 = gr.Button("Następny")
        back_btn1 = gr.Button("Powrót")

    # Moduł 2
    with gr.Row(visible=False, elem_id="mod2") as mod2_view:
        title2 = gr.Textbox(label="Tytuł", interactive=False)
        desc2 = gr.Textbox(label="Opis", interactive=False)
        img2 = gr.HTML()
        step2 = gr.Number(value=0, visible=False)
        with gr.Row():
            prev_btn2 = gr.Button("Poprzedni")
            next_btn2 = gr.Button("Następny")
        back_btn2 = gr.Button("Powrót")

    # Moduł 3
    with gr.Row(visible=False, elem_id="mod3") as mod3_view:
        title3 = gr.Textbox(label="Tytuł", interactive=False)
        desc3 = gr.Textbox(label="Opis", interactive=False)
        img3 = gr.HTML()
        step3 = gr.Number(value=0, visible=False)
        with gr.Row():
            prev_btn3 = gr.Button("Poprzedni")
            next_btn3 = gr.Button("Następny")
        back_btn3 = gr.Button("Powrót")

    # Nawigacja między ekranami
    def show_mod(mod_id):
        return {
            "mod1": [gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)],
            "mod2": [gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)],
            "mod3": [gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)],
        }[mod_id]

    def back_to_home():
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

    # Obsługa kliknięć ikon
    icon1.click(lambda: show_mod("mod1"), outputs=[mod1_view, mod2_view, mod3_view])
    icon2.click(lambda: show_mod("mod2"), outputs=[mod1_view, mod2_view, mod3_view])
    icon3.click(lambda: show_mod("mod3"), outputs=[mod1_view, mod2_view, mod3_view])
    back_btn1.click(back_to_home, outputs=[mod1_view, mod2_view, mod3_view])
    back_btn2.click(back_to_home, outputs=[mod1_view, mod2_view, mod3_view])
    back_btn3.click(back_to_home, outputs=[mod1_view, mod2_view, mod3_view])

    # Nawigacja w slajdach
    def update_slides(module, step):
        return module(step)

    next_btn1.click(lambda x: x + 1, inputs=[step1], outputs=[step1])
    prev_btn1.click(lambda x: x - 1, inputs=[step1], outputs=[step1])
    next_btn1.click(lambda x: module_1(int(x)), inputs=[step1], outputs=[title1, desc1, img1])
    prev_btn1.click(lambda x: module_1(int(x)), inputs=[step1], outputs=[title1, desc1, img1])

    next_btn2.click(lambda x: x + 1, inputs=[step2], outputs=[step2])
    prev_btn2.click(lambda x: x - 1, inputs=[step2], outputs=[step2])
    next_btn2.click(lambda x: module_2(int(x)), inputs=[step2], outputs=[title2, desc2, img2])
    prev_btn2.click(lambda x: module_2(int(x)), inputs=[step2], outputs=[title2, desc2, img2])

    next_btn3.click(lambda x: x + 1, inputs=[step3], outputs=[step3])
    prev_btn3.click(lambda x: x - 1, inputs=[step3], outputs=[step3])
    next_btn3.click(lambda x: module_3(int(x)), inputs=[step3], outputs=[title3, desc3, img3])
    prev_btn3.click(lambda x: module_3(int(x)), inputs=[step3], outputs=[title3, desc3, img3])

demo.launch()
