import tkinter as tk
from simulation import simulation_window
from helpers import mark_direct_slides_as_viewed, mark_coherent_slides_as_viewed

def show_direct_detection(menu_window, update_final_button):
    slides = [
        ("text_image", "wtie.png", "Detekcja bezpośrednia - slajd 1"),
        ("simulation", "Detekcja Bezpośrednia", "Interaktywna symulacja detekcji bezpośredniej")
    ]
    show_window_sequence(slides, "Direct Detection", lambda: [mark_direct_slides_as_viewed(), update_final_button()])

def show_coherent_detection(menu_window, update_final_button):
    slides = [
        ("text_image", "wtie.png", "Detekcja koherentna - slajd 1"),
        ("simulation", "Detekcja Koherentna", "Interaktywna symulacja detekcji koherentnej")
    ]
    show_window_sequence(slides, "Coherent Detection", lambda: [mark_coherent_slides_as_viewed(), update_final_button()])

def show_window_sequence(slides, title, on_finish):
    def create_slide_window(index):
        slide_window = tk.Toplevel()
        slide_window.attributes('-fullscreen', True)
        slide_window.title(title)

        slide_type, content, slide_text = slides[index]

        # Wyświetlanie tekstu slajdu
        text_label = tk.Label(slide_window, text=slide_text, font=("Helvetica", 16))
        text_label.pack(pady=10)

        # Wyświetlanie zawartości slajdu (obrazek lub symulacja)
        if slide_type == "text_image":
            try:
                img = tk.PhotoImage(file=content)
                image_label = tk.Label(slide_window, image=img)
                image_label.image = img
                image_label.pack(pady=20)
            except tk.TclError:
                tk.messagebox.showerror("Błąd", f"Nie znaleziono pliku {content}")
        elif slide_type == "simulation":
            sim_button = tk.Button(
                slide_window,
                text="Uruchom symulację",
                font=("Arial", 14),
                command=lambda: simulation_window(slide_window, content)
            )
            sim_button.pack(pady=20)

        # Dodanie dolnej ramki nawigacji
        nav_frame = tk.Frame(slide_window, bg="lightgray")
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Funkcja przejścia do kolejnego slajdu
        def next_slide():
            slide_window.destroy()
            if index < len(slides) - 1:
                create_slide_window(index + 1)
            else:
                on_finish()

        # Funkcja powrotu do poprzedniego slajdu
        def previous_slide():
            slide_window.destroy()
            if index > 0:
                create_slide_window(index - 1)

        # Przyciski nawigacyjne
        back_button = tk.Button(
            nav_frame,
            text="Wstecz",
            font=("Arial", 14),
            command=previous_slide
        )
        back_button.pack(side=tk.LEFT, padx=20, pady=10)
        back_button.config(state=tk.NORMAL if index > 0 else tk.DISABLED)

        next_button = tk.Button(
            nav_frame,
            text="Dalej" if index < len(slides) - 1 else "Zakończ",
            font=("Arial", 14),
            command=next_slide
        )
        next_button.pack(side=tk.RIGHT, padx=20, pady=10)

    # Rozpoczęcie od pierwszego slajdu
    create_slide_window(0)

