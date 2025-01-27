import gradio as gr
import numpy as np
import matplotlib.pyplot as plt

def button_click(button_name):
    # Ukrywanie menu i przełączanie widoczności zakładek
    if button_name == "1":
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    elif button_name == "2":
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
    elif button_name == "3":
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

def update_plots(param1, param2):
    x = np.linspace(0, 10, 500)
    y1 = np.sin(param1 * x)
    y2 = np.cos(param2 * x)

    fig, ax = plt.subplots(2, 1, figsize=(6, 8))
    ax[0].plot(x, y1, label=f"sin({param1}x)")
    ax[0].legend()
    ax[0].set_title("Wykres sinusoidy")

    ax[1].plot(x, y2, label=f"cos({param2}x)", color='orange')
    ax[1].legend()
    ax[1].set_title("Wykres cosinusoidy")

    plt.tight_layout()
    return fig

# Ścieżki do grafik
logo_path = "wtie.png"
icon1_path = "1-png.png"
icon2_path = "2-png.png"
icon3_path = "3-png.png"

# Tworzenie interfejsu Gradio
with gr.Blocks() as app:
    # Menu główne
    with gr.Row(visible=True) as menu:
        gr.Image(logo_path, elem_id="logo", show_label=False)

        with gr.Row():
            btn1 = gr.Button("Przycisk 1")
            btn2 = gr.Button("Przycisk 2")
            btn3 = gr.Button("Przycisk 3")

        with gr.Row():
            gr.Image(icon1_path, elem_id="icon1", show_label=False, interactive=False)
            gr.Image(icon2_path, elem_id="icon2", show_label=False)
            gr.Image(icon3_path, elem_id="icon3", show_label=False)

    # Zakładka 1
    with gr.Column(visible=False) as tab1:
        gr.Markdown("## Zakładka 1 - Interaktywna Symulacja")
        slider1 = gr.Slider(1, 10, step=1, label="Parametr 1")
        slider2 = gr.Slider(1, 10, step=1, label="Parametr 2")
        plot1 = gr.Plot()

        slider1.change(fn=update_plots, inputs=[slider1, slider2], outputs=plot1)
        slider2.change(fn=update_plots, inputs=[slider1, slider2], outputs=plot1)

    # Zakładka 2
    with gr.Column(visible=False) as tab2:
        gr.Markdown("## Zakładka 2 - Treść do rozwinięcia")
        gr.Textbox("Tutaj możesz dodać kolejne symulacje lub informacje.", lines=3)

    # Zakładka 3
    with gr.Column(visible=False) as tab3:
        gr.Markdown("## Zakładka 3 - Treść do rozwinięcia")
        gr.Textbox("Tutaj możesz dodać kolejne symulacje lub informacje.", lines=3)

    # Obsługa kliknięć w menu
    btn1.click(fn=button_click, inputs=[gr.Textbox(value="1")], outputs=[menu, tab1, tab2, tab3])
    btn2.click(fn=button_click, inputs=[gr.Textbox(value="2")], outputs=[menu, tab1, tab2, tab3])
    btn3.click(fn=button_click, inputs=[gr.Textbox(value="3")], outputs=[menu, tab1, tab2, tab3])

# Uruchomienie aplikacji
app.launch()