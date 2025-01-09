import json
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
import numpy as np
import subprocess

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

# Funkcja do obsługi symulacji (z użyciem subprocess)
def create_simulation_window(simulation):
    try:
        script_path = simulation["script_path"]
        if not script_path:
            raise ValueError("Brak ścieżki do pliku symulacji w konfiguracji.")

        subprocess.run(["python", script_path], check=True)
    except Exception as e:
        print(f"[ERROR] Nie udało się uruchomić symulacji: {e}")
        tk.messagebox.showerror("Błąd", f"Nie udało się uruchomić symulacji: {e}")

# Funkcja do wyświetlania sekwencji slajdów
def show_window_sequence(slides, title):
    if not slides:
        print("[ERROR] No slides to display")
        return

    root = tk.Toplevel(bg="white")
    root.attributes('-fullscreen', True)
    root.title(title)

    # Ramki dla treści i nawigacji
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(expand=True, fill=tk.BOTH)

    nav_frame = tk.Frame(root, bg="white")
    nav_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    current_index = {"index": 0}  # Użycie słownika, aby umożliwić mutowalność

    def update_slide():
        """Aktualizuje zawartość okna dla bieżącego slajdu"""
        for widget in content_frame.winfo_children():
            widget.destroy()

        slide = slides[current_index["index"]]

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

            elif element["type"] == "highlighted_text":
                bold = "bold" if element.get("bold", False) else "normal"
                text_color = element.get("text_color", "black")
                background_color = element.get("background_color", "lightgray")

                highlight_label = tk.Label(
                    content_frame,
                    text=element["content"],
                    font=("Helvetica", 16, bold),
                    wraplength=1000,
                    justify="left",
                    fg=text_color,
                    bg=background_color,
                    padx=10,
                    pady=10
                )
                highlight_label.pack(pady=10)

            elif element["type"] == "image":
                image_path = element["content"]
                try:
                    img = Image.open(image_path)
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

            elif element["type"] == "simulation":
                label = element["content"].get("label", "Uruchom symulację")
                button = tk.Button(
                    content_frame,
                    text=label,
                    command=lambda sim=element["content"]: create_simulation_window(sim),
                    bg="white"
                )
                button.pack(pady=10)

        # Aktualizacja stanu przycisku "Wstecz"
        if current_index["index"] == 0:
            back_button.config(state=tk.DISABLED)
        else:
            back_button.config(state=tk.NORMAL)

    def next_slide():
        """Przechodzi do następnego slajdu"""
        if current_index["index"] < len(slides) - 1:
            current_index["index"] += 1
            update_slide()
        else:
            root.destroy()

    def previous_slide():
        """Przechodzi do poprzedniego slajdu"""
        if current_index["index"] > 0:
            current_index["index"] -= 1
            update_slide()

    # Przyciski nawigacyjne
    back_button = tk.Button(nav_frame, text="Wstecz", command=previous_slide, bg="white")
    back_button.pack(side=tk.LEFT, padx=20, pady=10)

    next_button = tk.Button(nav_frame, text="Dalej", command=next_slide, bg="white")
    next_button.pack(side=tk.RIGHT, padx=20, pady=10)

    # Inicjalizacja pierwszego slajdu
    update_slide()
