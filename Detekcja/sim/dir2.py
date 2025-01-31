import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class Simulation:
    def __init__(self):
        # Parametry początkowe
        self.fs = 1000
        self.f_carrier = 150
        self.f_mod = 5
        self.amplitude = 1
        self.responsivity = 0.5
        self.cutoff_freq = 20
        self.time_base = 1.0

        self.t = np.linspace(0, self.time_base, int(self.fs * self.time_base))
        self.update_signals()

        # Tworzenie wykresów Matplotlib
        self.fig, self.axs = plt.subplots(3, 1, figsize=(6, 5))
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
        self.E_t = self.amplitude * (1 + 0.5 * np.sin(2 * np.pi * self.f_mod * self.t)) * np.sin(2 * np.pi * self.f_carrier * self.t)
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
        self.axs[0].set_title('Sygnał optyczny E(t)')
        self.line_E, = self.axs[0].plot(self.t, self.E_t, label='E(t)')
        self.axs[0].legend()
        self.axs[0].grid()

        self.axs[1].set_title('Moc optyczna P(t)')
        self.line_P, = self.axs[1].plot(self.t, self.P_t, label='P(t)', color='orange')
        self.axs[1].legend()
        self.axs[1].grid()

        self.axs[2].set_title('Prąd fotodetektora I(t)')
        self.line_I_raw, = self.axs[2].plot(self.t, self.I_t, label='I(t) - bez filtra', color='red', alpha=0.7)
        self.line_I_filtered, = self.axs[2].plot(self.t, self.I_t_filtered, label='I(t) - po filtrze', color='green')
        self.axs[2].legend()
        self.axs[2].grid()

        self.fig.canvas.draw()

    def update_plot(self):
        """Aktualizuje wykresy po zmianie parametrów"""
        self.update_signals()

        self.line_E.set_data(self.t, self.E_t)
        self.line_P.set_data(self.t, self.P_t)
        self.line_I_raw.set_data(self.t, self.I_t)
        self.line_I_filtered.set_data(self.t, self.I_t_filtered)

        self.axs[0].set_xlim(0, self.time_base)
        self.axs[1].set_xlim(0, self.time_base)
        self.axs[2].set_xlim(0, self.time_base)

        self.fig.canvas.draw()