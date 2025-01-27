import gradio as gr

def to_uppercase(text):
    return text.upper()

interface = gr.Interface(
    fn=to_uppercase,                # Funkcja do wykonania
    inputs=gr.Textbox(label="Input Text"), # Wejście
    outputs=gr.Textbox(label="Output Text") # Wyjście
)

interface.launch(share=True)

interface.launch()  # Uruchom aplikację