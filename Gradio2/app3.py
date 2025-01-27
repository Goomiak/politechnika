import gradio as gr

# Przykładowe dane slajdów
slides = [
    {
        "title": "Slajd 1",
        "texts": ["Tekst 1A", "Tekst 1B", "Tekst 1C"],
        "image": "1-png.png"
    },
    {
        "title": "Slajd 2",
        "texts": ["Tekst 2A", "Tekst 2B"],
        "image": "2-png.png"
    },
    {
        "title": "Slajd 3",
        "texts": ["Tekst 3A", "Tekst 3B", "Tekst 3C", "Tekst 3D"],
        "image": "3-png.png"
    }
]

# Funkcja do dynamicznego generowania slajdu
def show_slide(slide_index, direction):
    if direction == "next":
        slide_index = (slide_index + 1) % len(slides)
    elif direction == "previous":
        slide_index = (slide_index - 1) % len(slides)

    slide = slides[slide_index]
    title = slide["title"]
    texts = slide["texts"]
    image = slide["image"]

    # Tworzymy dynamiczną listę wyjść: tytuł, teksty, obraz, indeks slajdu
    outputs = [title]
    outputs.extend(texts)
    outputs.append(image)
    outputs.append(slide_index)
    return outputs


# Interfejs Gradio
with gr.Blocks() as demo:
    slide_index = gr.State(0)

    # Dynamiczne komponenty interfejsu
    title = gr.Textbox(label="Tytuł", interactive=False)

    # Placeholder na dynamiczne teksty i obraz
    dynamic_texts = gr.Group()
    image = gr.Image(label="Obraz", interactive=False)

    # Przyciski
    btn_previous = gr.Button("Poprzedni")
    btn_next = gr.Button("Następny")

    # Funkcja do aktualizacji interfejsu
    def update_ui(slide_index, direction):
        slide_data = show_slide(slide_index, direction)
        title.update(value=slide_data[0])
        
        # Dynamiczne tworzenie pól tekstowych
        dynamic_texts.clear()
        for text in slide_data[1:-2]:  # Pomijamy obraz i indeks slajdu
            gr.Textbox(value=text, label="Tekst", interactive=False, parent=dynamic_texts)

        image.update(value=slide_data[-2])
        return slide_data[-1]  # Aktualizacja indeksu slajdu

    # Powiązanie przycisków z funkcją
    btn_previous.click(
        fn=update_ui,
        inputs=[slide_index, gr.State("previous")],
        outputs=[slide_index]
    )

    btn_next.click(
        fn=update_ui,
        inputs=[slide_index, gr.State("next")],
        outputs=[slide_index]
    )

# Uruchomienie aplikacji
demo.launch()