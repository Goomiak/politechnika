import gradio as gr

def button_click(button_name):
    return f"Kliknięto przycisk: {button_name}"

# Ścieżki do grafik
logo_path = "wtie.png"
icon1_path = "1-png.png"
icon2_path = "2-png.png"
icon3_path = "3-png.png"

# Tworzenie interfejsu Gradio
with gr.Blocks() as app:
    # Logo na samej górze
    gr.Image(logo_path, elem_id="logo", show_label=False)

    # Przyciski w jednym rzędzie
    with gr.Row():
        btn1 = gr.Button("Przycisk 1")
        btn2 = gr.Button("Przycisk 2")
        btn3 = gr.Button("Przycisk 3")

    # Ikonki w kolejnym rzędzie
    with gr.Row():
        gr.Image(icon1_path, elem_id="icon1", show_label=False)
        gr.Image(icon2_path, elem_id="icon2", show_label=False)
        gr.Image(icon3_path, elem_id="icon3", show_label=False)

    # Wyświetlanie wiadomości po kliknięciu przycisku
    output = gr.Textbox(label="Informacja zwrotna")

    # Funkcje obsługi przycisków
    btn1.click(fn=lambda: button_click("Przycisk 1"), inputs=None, outputs=output)
    btn2.click(fn=lambda: button_click("Przycisk 2"), inputs=None, outputs=output)
    btn3.click(fn=lambda: button_click("Przycisk 3"), inputs=None, outputs=output)

# Uruchomienie aplikacji
app.launch(share=True)