import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def simulation_window(slide_window, simulation_type):
    slide_window.destroy()

    sim_window = tk.Toplevel()
    sim_window.attributes('-fullscreen', True)
    sim_window.title(f"Symulacja - {simulation_type}")

    param_frame = tk.Frame(sim_window)
    param_frame.pack(side=tk.TOP, pady=20)

    param_label = tk.Label(param_frame, text="Wprowadź parametry symulacji:", font=("Arial", 16))
    param_label.pack()

    param_amplitude_label = tk.Label(param_frame, text="Amplituda sygnału:", font=("Arial", 14))
    param_amplitude_label.pack(side=tk.LEFT, padx=5)
    param_amplitude = tk.Entry(param_frame, width=10)
    param_amplitude.pack(side=tk.LEFT, padx=5)

    param_frequency_label = tk.Label(param_frame, text="Częstotliwość [Hz]:", font=("Arial", 14))
    param_frequency_label.pack(side=tk.LEFT, padx=5)
    param_frequency = tk.Entry(param_frame, width=10)
    param_frequency.pack(side=tk.LEFT, padx=5)

    param_noise_label = tk.Label(param_frame, text="Poziom szumu:", font=("Arial", 14))
    param_noise_label.pack(side=tk.LEFT, padx=5)
    param_noise = tk.Entry(param_frame, width=10)
    param_noise.pack(side=tk.LEFT, padx=5)

    figure = plt.Figure(figsize=(10, 5), dpi=100)
    ax = figure.add_subplot(111)
    canvas = FigureCanvasTkAgg(figure, sim_window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot_simulation():
        try:
            amplitude = float(param_amplitude.get())
            frequency = float(param_frequency.get())
            noise_level = float(param_noise.get())

            t = np.linspace(0, 1, 1000)
            signal = amplitude * np.sin(2 * np.pi * frequency * t)
            noise = noise_level * np.random.normal(size=t.shape)

            if simulation_type == "Detekcja Koherentna":
                coherent_signal = signal + noise
                ax.clear()
                ax.plot(t, coherent_signal, label="Sygnał koherentny")
            elif simulation_type == "Detekcja Bezpośrednia":
                detected_signal = np.abs(signal) + noise
                ax.clear()
                ax.plot(t, detected_signal, label="Sygnał bezpośredni")

            ax.set_title(f"Symulacja - {simulation_type}")
            ax.set_xlabel("Czas [s]")
            ax.set_ylabel("Amplituda")
            ax.legend()
            canvas.draw()
        except ValueError:
            tk.messagebox.showerror("Błąd", "Proszę wprowadzić poprawne wartości liczbowe.")

    plot_button = tk.Button(sim_window, text="Rysuj wykres", font=("Arial", 14), command=plot_simulation)
    plot_button.pack(pady=10)

    def back_to_menu():
        sim_window.destroy()

    back_button = tk.Button(sim_window, text="Powrót do menu", font=("Arial", 14), command=back_to_menu)
    back_button.pack(pady=10)
