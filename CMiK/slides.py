import json
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO

# Funkcja do wczytywania konfiguracji z pliku JSON
def load_config(config_path="config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Funkcja do generowania obrazu z wzoru matematycznego
def generate_math_image(math_expression):
    plt.figure(figsize=(2, 1))
    plt.text(0.5, 0.5, math_expression, fontsize=20, ha='center', va='center')
    plt.axis('off')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    return Image.open(buffer)

# Funkcja do wyświetlania sekwencji slajdów
def show_window_sequence(slides, title):
    def create_slide_window(index):
        slide_window = tk.Toplevel()
        slide_window.attributes('-fullscreen', True)
        slide_window.title(title)

        slide = slides[index]

        for element in slide["elements"]:
            if element["type"] == "text":
                text_label = tk.Label(
                    slide_window,
                    text=element["content"],
                    font=("Helvetica", 16),
                    wraplength=1000,
                    justify="left"
                )
                text_label.pack(pady=10)

            elif element["type"] == "image":
                image_path = element["content"]
                img = Image.open(image_path)
                img = img.resize((600, 400), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                image_label = tk.Label(slide_window, image=img_tk)
                image_label.image = img_tk  # Zachowaj referencję do obrazu
                image_label.pack(pady=10)

            elif element["type"] == "math":
                math_img = generate_math_image(element["content"])
                math_tk = ImageTk.PhotoImage(math_img)
                math_label = tk.Label(slide_window, image=math_tk)
                math_label.image = math_tk  # Zachowaj referencję do obrazu
                math_label.pack(pady=10)

        # Nawigacja
        nav_frame = tk.Frame(slide_window)
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)

        def next_slide():
            slide_window.destroy()
            if index < len(slides) - 1:
                create_slide_window(index + 1)

        def previous_slide():
            slide_window.destroy()
            if index > 0:
                create_slide_window(index - 1)

        back_button = tk.Button(nav_frame, text="Wstecz", command=previous_slide)
        back_button.pack(side=tk.LEFT, padx=20, pady=20)
        back_button.config(state=tk.NORMAL if index > 0 else tk.DISABLED)

        next_button = tk.Button(nav_frame, text="Dalej", command=next_slide)
        next_button.pack(side=tk.RIGHT, padx=20, pady=20)
        next_button.config(text="Zakończ" if index == len(slides) - 1 else "Dalej")

    create_slide_window(0)
