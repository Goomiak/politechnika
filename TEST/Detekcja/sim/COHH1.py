import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class Simulation:
    def __init__(self):
        # Parametry symulacji
        self.fs = 1000  # Częstotliwość próbkowania
        self.f_carrier = 150  # Częstotliwość nośna [THz]
        self.f_mod = 5  # Częstotliwość modulacji [GHz]
        self.amplitude_signal = 10  # Moc sygnału optycznego [mW]
        self.amplitude_LO = 1  # Moc lokalnego oscylatora [mW]
        self.phase_difference = np.pi / 4  # Początkowa różnica fazowa
        self.time_base = 1.0  # Okno czasowe [ps]

        self.t = np.linspace(0, self.time_base, int(self.fs * self.time_base))
        self.update_signals()

        # Tworzenie wykresów Matplotlib
        self.fig, self.axs = plt.subplots(3, 1, figsize=(6, 7), sharex=True)
        self.fig.subplots_adjust(hspace=0.5)
        self.plot_signals()

    def update_parameter(self, param_name, value):
        """Aktualizuje parametr symulacji"""
        if param_name == "Moc LO [mW]":
            self.amplitude_LO = value
        elif param_name == "Faza LO [rad]":
            self.phase_difference = value
        elif param_name == "Częstotliwość [THz]":
            self.f_carrier = value
        elif param_name == "Podstawa czasu [ps]":
            self.time_base = value
            self.t = np.linspace(0, self.time_base, int(self.fs * self.time_base))
        
        self.update_plot()

    def update_signals(self):
        """Oblicza nowe wartości sygnałów."""
        E_opt = np.sqrt(self.amplitude_signal) * np.sin(2 * np.pi * self.f_carrier * self.t)
        E_LO = np.sqrt(self.amplitude_LO) * np.sin(2 * np.pi * self.f_carrier * self.t + self.phase_difference)
        
        # Interferencja na detektorze
        E_total = E_opt + E_LO
        self.P_t = np.abs(E_total) ** 2  # Moc optyczna na detektorze
        self.I_t = self.P_t  # Prąd fotodetektora
        self.I_t_filtered = self.lowpass_filter(self.I_t, 20, self.fs)

    def lowpass_filter(self, data, cutoff, fs, order=2):
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return filtfilt(b, a, data)

    def plot_signals(self):
        """Tworzy wykresy."""
        self.axs[0].set_title('Sygnał optyczny i lokalny oscylator')
        self.line_E_opt, = self.axs[0].plot(self.t, np.sqrt(self.amplitude_signal) * np.sin(2 * np.pi * self.f_carrier * self.t), label='E_opt')
        self.line_E_LO, = self.axs[0].plot(self.t, np.sqrt(self.amplitude_LO) * np.sin(2 * np.pi * self.f_carrier * self.t + self.phase_difference), label='E_LO', linestyle='dashed')
        self.axs[0].legend()
        self.axs[0].grid()

        self.axs[1].set_title('Moc optyczna P(t)')
        self.line_P, = self.axs[1].plot(self.t, self.P_t, label='P(t)', color='orange')
        self.axs[1].legend()
        self.axs[1].grid()

        self.axs[2].set_title('Prąd fotodetektora I(t)')
        self.line_I_filtered, = self.axs[2].plot(self.t, self.I_t_filtered, label='I(t) - po filtrze', color='green')
        self.axs[2].legend()
        self.axs[2].grid()

        self.fig.canvas.draw()

    def update_plot(self):
        """Aktualizuje wykresy po zmianie parametrów."""
        self.update_signals()
        self.line_E_opt.set_data(self.t, np.sqrt(self.amplitude_signal) * np.sin(2 * np.pi * self.f_carrier * self.t))
        self.line_E_LO.set_data(self.t, np.sqrt(self.amplitude_LO) * np.sin(2 * np.pi * self.f_carrier * self.t + self.phase_difference))
        self.line_P.set_data(self.t, self.P_t)
        self.line_I_filtered.set_data(self.t, self.I_t_filtered)

        self.axs[0].set_xlim(0, self.time_base)
        self.axs[1].set_xlim(0, self.time_base)
        self.axs[2].set_xlim(0, self.time_base)

        self.fig.canvas.draw()