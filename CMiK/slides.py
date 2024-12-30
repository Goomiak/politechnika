import json
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO

# Funkcja do wczytywania konfiguracji z pliku JSON
def load_config(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            print("[DEBUG] Config loaded successfully:", config)
            return config
    except Exception as e:
        print(f"[ERROR] Failed to load config: {e}")
        raise

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
    if not slides:
        print("[ERROR] No slides to display")
        return

    def create_slide_window(index):
        print(f"[DEBUG] Showing slide {index + 1}/{len(slides)}")

        slide_window = tk.Toplevel(bg="white")
        slide_window.attributes('-fullscreen', True)
        slide_window.title(title)

        # Podział na ramki treści i nawigacji
        content_frame = tk.Frame(slide_window, bg="white")
        content_frame.pack(expand=True, fill=tk.BOTH)

        nav_frame = tk.Frame(slide_window, bg="white")
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        slide = slides[index]

        # Wyświetlanie zawartości slajdu
        for element in slide.get("elements", []):
            if element["type"] == "text":
                text_label = tk.Label(
                    content_frame,
                    text=element["content"],
                    font=("Helvetica", 16),
                    wraplength=1000,
                    justify="left",
                    bg="white"
                )
                text_label.pack(pady=10)

            elif element["type"] == "image":
                image_path = element["content"]
                try:
                    img = Image.open(image_path)
                    img = img.resize((600, 400), Image.Resampling.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)
                    image_label = tk.Label(content_frame, image=img_tk, bg="white")
                    image_label.image = img_tk  # Zachowaj referencję do obrazu
                    image_label.pack(pady=10)
                except Exception as e:
                    print(f"[ERROR] Failed to load image {image_path}: {e}")

            elif element["type"] == "math":
                math_img = generate_math_image(element["content"])
                math_tk = ImageTk.PhotoImage(math_img)
                math_label = tk.Label(content_frame, image=math_tk, bg="white")
                math_label.image = math_tk  # Zachowaj referencję do obrazu
                math_label.pack(pady=10)

        # Dodanie nawigacji
        def next_slide():
            if index < len(slides) - 1:
                print("[DEBUG] Moving to next slide")
                slide_window.destroy()
                create_slide_window(index + 1)

        def previous_slide():
            if index > 0:
                print("[DEBUG] Moving to previous slide")
                slide_window.destroy()
                create_slide_window(index - 1)

        back_button = tk.Button(nav_frame, text="Wstecz", command=previous_slide, bg="white")
        back_button.pack(side=tk.LEFT, padx=20, pady=10)
        back_button.config(state=tk.NORMAL if index > 0 else tk.DISABLED)

        next_button = tk.Button(nav_frame, text="Dalej", command=next_slide, bg="white")
        next_button.pack(side=tk.RIGHT, padx=20, pady=10)
        next_button.config(text="Zakończ" if index == len(slides) - 1 else "Dalej")

    create_slide_window(0)
