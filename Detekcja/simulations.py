import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class BaseSimulation:
    """Bazowa klasa symulacji"""
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))

    def update_parameter(self, param_name, value):
        """Metoda do nadpisania w podklasach"""
        pass

class DirectDetectionSimulation(BaseSimulation):
    """Symulacja detekcji bezpośredniej"""
    def __init__(self):
        super().__init__()
        self.fs = 1000  # Częstotliwość próbkowania
        self.f_carrier = 150  # Częstotliwość nośna [THz]
        self.amplitude = 1  # Amplituda sygnału
        self.time_base = 1.0  # Podstawa czasu [ps]
        self.responsivity = 0.5  # Czułość detektora
        self.cutoff_freq = 20  # Częstotliwość odcięcia filtru

        self.t = np.linspace(0, self.time_base, int(self.fs * self.time_base))
        self.update_signals()
        self.plot_signals()

    def update_parameter(self, param_name, value):
        """Aktualizuje parametr symulacji"""
        if param_name == "Amplituda":
            self.amplitude = value
        elif param_name == "Częstotliwość [THz]":
            self.f_carrier = value
        elif param_name == "Podstawa czasu [ps]":
            self.time_base = value
            self.t = np.linspace(0, self.time_base, int(self.fs * self.time_base))
        
        self.update_plot()

    def update_signals(self):
        """Oblicza nowe wartości sygnałów"""
        self.E_t = self.amplitude * (1 + 0.5 * np.sin(2 * np.pi * 5 * self.t)) * np.sin(2 * np.pi * self.f_carrier * self.t)
        self.P_t = np.abs(self.E_t) ** 2
        self.I_t = self.responsivity * self.P_t
        self.I_t_filtered = self.lowpass_filter(self.I_t, self.cutoff_freq, self.fs)

    def lowpass_filter(self, data, cutoff, fs, order=2):
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return filtfilt(b, a, data)

    def plot_signals(self):
        """Tworzy wykresy"""
        self.ax.clear()
        self.ax.plot(self.t, self.I_t_filtered, label="Prąd fotodetektora")
        self.ax.legend()
        self.fig.canvas.draw()

    def update_plot(self):
        """Aktualizuje wykresy po zmianie parametrów"""
        self.update_signals()
        self.plot_signals()

# Słownik mapujący nazwy symulacji do klas
SIMULATION_CLASSES = {
    "direct_detection": DirectDetectionSimulation
}
