import json
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
import numpy as np

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

# Funkcja do obsługi symulacji
def create_simulation_window(simulation):
    sim_window = tk.Toplevel(bg="white")
    sim_window.title(simulation["name"])

    # Wymiary okna
    window_width = 800
    window_height = 600

    # Pobranie rozmiaru ekranu
    screen_width = sim_window.winfo_screenwidth()
    screen_height = sim_window.winfo_screenheight()

    # Wyliczenie pozycji okna na środku ekranu
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Ustawienie wymiarów i pozycji okna
    sim_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Tworzenie zawartości okna
    params = simulation.get("parameters", {})
    param_vars = {key: tk.DoubleVar(value=val.get("default", 0)) for key, val in params.items()}
    inputs = simulation.get("inputs", {})
    input_vars = {key: tk.StringVar(value=val.get("default", "")) for key, val in inputs.items()}

    figures = []
    for fig_conf in simulation.get("figures", []):
        fig, ax = plt.subplots(figsize=fig_conf.get("size", (6, 4)))
        figures.append((fig, ax))

    def update_simulation(*args):
        for fig, ax, fig_conf in zip([f[0] for f in figures], [f[1] for f in figures], simulation.get("figures", [])):
            ax.clear()
            exec(fig_conf.get("code", ""), {
                **param_vars,
                **input_vars,
                "np": np,
                "plt": plt,
                "ax": ax
            })
        for canvas in canvases:
            canvas.draw()

    # Ramka na całość (dla wyśrodkowania panelu sterowania)
    main_frame = tk.Frame(sim_window, bg="white")
    main_frame.pack(expand=True, fill=tk.BOTH)

    # Panel sterowania parametrami
    control_frame = tk.Frame(main_frame, bg="white")
    control_frame.pack(side=tk.TOP, pady=10)

    for param, config in params.items():
        frame = tk.Frame(control_frame, bg="white")
        frame.pack(pady=5)

        label = tk.Label(frame, text=f"{param.capitalize()}: ", bg="white", font=("Arial", 12))
        label.pack(side=tk.LEFT, padx=10)

        scale = tk.Scale(
            frame, from_=config["min"], to=config["max"], resolution=config["step"],
            variable=param_vars[param], orient=tk.HORIZONTAL, bg="white", length=400
        )
        scale.pack(side=tk.LEFT, padx=10)

        param_vars[param].trace_add("write", update_simulation)

    for inp, config in inputs.items():
        frame = tk.Frame(control_frame, bg="white")
        frame.pack(pady=5)

        label = tk.Label(frame, text=f"{inp.capitalize()}: ", bg="white", font=("Arial", 12))
        label.pack(side=tk.LEFT, padx=10)

        entry = tk.Entry(frame, textvariable=input_vars[inp], font=("Arial", 12), width=20)
        entry.pack(side=tk.LEFT, padx=10)

        input_vars[inp].trace_add("write", update_simulation)

    # Wykresy
    canvas_frame = tk.Frame(main_frame, bg="white")
    canvas_frame.pack(expand=True, fill=tk.BOTH)

    canvases = []
    for fig, _ in figures:
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvases.append(canvas)

    update_simulation()

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
                   # img = img.resize((800, 300), Image.Resampling.LANCZOS)
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
                button = tk.Button(
                    content_frame,
                    text=f"Uruchom symulację - {element['content']['name']}",
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
