import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)

        self.root.title("TECHNIKI RF - Symulacje")
        
        # Lista symulacji
        self.simulations = {
            "Transmisja RF": self.simulation_rf_transmission,
            "Tłumienie w światłowodzie": self.simulation_optical_attenuation,
        }
        
        # Parametry
        self.params = {
            "f_rf": tk.DoubleVar(value=5e3),
            "f_light": tk.DoubleVar(value=2e5),
            "attenuation": tk.DoubleVar(value=0.2),
            "distance": tk.DoubleVar(value=100),
        }
        
        # Tworzenie interfejsu
        self.create_widgets()
        self.current_simulation = list(self.simulations.keys())[0]
        self.update_simulation()
    
    def create_widgets(self):
        # Dropdown do wyboru symulacji
        ttk.Label(self.root, text="Wybierz symulację:").grid(row=0, column=0, sticky="w")
        self.simulation_choice = ttk.Combobox(self.root, values=list(self.simulations.keys()), state="readonly")
        self.simulation_choice.grid(row=0, column=1, sticky="ew")
        self.simulation_choice.set(list(self.simulations.keys())[0])
        self.simulation_choice.bind("<<ComboboxSelected>>", self.on_simulation_change)
        
        # Kontrolki do zmiany parametrów
        row = 1
        for param, var in self.params.items():
            ttk.Label(self.root, text=f"{param}:").grid(row=row, column=0, sticky="w")
            ttk.Entry(self.root, textvariable=var).grid(row=row, column=1, sticky="ew")
            row += 1
        
        # Przycisk odśwież
        ttk.Button(self.root, text="Odśwież", command=self.update_simulation).grid(row=row, column=0, columnspan=2)
        
        # Miejsce na wykres
        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=1, column=2, rowspan=row+1, sticky="nsew")
    
    def on_simulation_change(self, event):
        self.current_simulation = self.simulation_choice.get()
        self.update_simulation()
    
    def update_simulation(self):
        # Czyści aktualny wykres
        self.figure.clear()
        
        # Wywołuje wybraną symulację
        simulation_func = self.simulations.get(self.current_simulation)
        if simulation_func:
            simulation_func()
        
        # Aktualizuje płótno
        self.canvas.draw()
    
    def simulation_rf_transmission(self):
        f_rf = self.params["f_rf"].get()
        f_light = self.params["f_light"].get()
        
        t = np.linspace(0, 0.01, 1000)
        rf_signal = np.cos(2 * np.pi * f_rf * t)
        modulated_signal = (1 + rf_signal) * np.cos(2 * np.pi * f_light * t)
        
        ax1 = self.figure.add_subplot(211)
        ax1.plot(t, rf_signal)
        ax1.set_title("Sygnał RF")
        ax1.set_xlabel("Czas [s]")
        ax1.set_ylabel("Amplituda")
        
        ax2 = self.figure.add_subplot(212)
        ax2.plot(t, modulated_signal)
        ax2.set_title("Sygnał modulowany")
        ax2.set_xlabel("Czas [s]")
        ax2.set_ylabel("Amplituda")
    
    def simulation_optical_attenuation(self):
        attenuation = self.params["attenuation"].get()
        distance = self.params["distance"].get()
        
        distances = np.linspace(0, distance, 500)
        intensity = np.exp(-attenuation * distances)
        
        ax = self.figure.add_subplot(111)
        ax.plot(distances, intensity)
        ax.set_title("Tłumienie w światłowodzie")
        ax.set_xlabel("Odległość [km]")
        ax.set_ylabel("Natężenie sygnału")
        ax.grid()

# Uruchamianie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
