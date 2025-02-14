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

class DirectDetectionSimulation:
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
        self.fig, self.axs = plt.subplots(3, 1, figsize=(6, 7), sharex=True)
        self.fig.subplots_adjust(hspace=0.5)  # Zwiększenie odstępu między wykresami
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
        self.axs[0].set_ylim(np.min(self.E_t) - 0.5, np.max(self.E_t) + 0.5)
        self.axs[1].set_xlim(0, self.time_base)
        self.axs[1].set_ylim(np.min(self.P_t), np.max(self.P_t) + 0.5)
        self.axs[2].set_xlim(0, self.time_base)
        self.axs[2].set_ylim(min(np.min(self.I_t), np.min(self.I_t_filtered)), max(np.max(self.I_t), np.max(self.I_t_filtered)) + 0.5)

        self.fig.canvas.draw()

class CoherentDetectionSimulation:
    def __init__(self):
        self.fs = 5000
        self.f_c = 100
        self.f_LO = 100
        self.phi = 0
        self.fm = 5

        self.t = np.linspace(0, 1, int(self.fs * 1), endpoint=False)
        self.m = np.sin(2 * np.pi * self.fm * self.t)
        self.update_signals()
        self.fig, self.axs = plt.subplots(2, 1, figsize=(10, 6))
        self.plot_signals()

    def update_parameter(self, param_name, value):
        if param_name == "Nośna f_c [THz]":
            self.f_c = value
        elif param_name == "Błąd fazowy φ [rad]":
            self.phi = value
        self.update_plot()

    def update_signals(self):
        self.r = 0.5 * self.m * np.cos(2 * np.pi * (self.f_c - self.f_LO) * self.t - self.phi)

    def plot_signals(self):
        for ax in self.axs:
            ax.clear()
        self.axs[0].plot(self.t, self.m, label='Sygnał m(t)')
        self.axs[1].plot(self.t, self.r, label='Odzyskany sygnał r(t)', color='red')
        for ax in self.axs:
            ax.legend()
            ax.grid()
        self.fig.canvas.draw()

    def update_plot(self):
        self.update_signals()
        self.plot_signals()

class QAMSimulation:
    def __init__(self):
        # Parametry początkowe
        self.symbols = 64
        self.iterations = 10
        self.noise_std = 0.03

        # Tworzenie wykresu Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.update_plot()

    def generate_qam_constellation(self, N, iterations, noise_std):
        if not (np.log2(N) % 1 == 0):
            raise ValueError("N must be a power of 2 (e.g., 4, 16, 64, ...).")
        
        M = int(np.sqrt(N))
        if M * M != N:
            raise ValueError("N must have an integer square root (e.g., 4, 16, 64, ...).")

        x = np.arange(-M + 1, M, 2)
        y = np.arange(-M + 1, M, 2)
        xv, yv = np.meshgrid(x, y)
        base_constellation = xv.flatten() + 1j * yv.flatten()
        base_constellation /= np.sqrt(np.mean(np.abs(base_constellation) ** 2))

        jitter = noise_std * (np.random.randn(len(base_constellation) * iterations) + 1j * np.random.randn(len(base_constellation) * iterations))
        constellation = np.tile(base_constellation, iterations) + jitter
        return constellation

    def update_parameter(self, param_name, value):
        if param_name == "Liczba symboli":
            self.symbols = int(value)
        elif param_name == "Iteracje":
            self.iterations = int(value)
        elif param_name == "Szum (std)":
            self.noise_std = value
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        constellation = self.generate_qam_constellation(self.symbols, self.iterations, self.noise_std)
        self.ax.scatter(constellation.real, constellation.imag, c='blue', alpha=0.6)
        self.ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
        self.ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_title(f'QAM {self.symbols}-Symbol Constellation')
        self.ax.set_xlabel('In-Phase')
        self.ax.set_ylabel('Quadrature')
        self.ax.axis('equal')
        self.fig.canvas.draw()

class AMSimulation:
    def __init__(self):
        # Parametry początkowe
        self.Ac = 1.0  # Amplituda nośnej
        self.fc = 150.0  # Częstotliwość nośnej
        self.Am = 1.0  # Amplituda sygnału modulującego
        self.fm = 10.0  # Częstotliwość sygnału modulującego
        self.t = np.linspace(0, 1, 1000)

        # Tworzenie wykresu Matplotlib
        self.fig, self.axs = plt.subplots(3, 1, figsize=(6, 8), sharex=True)
        self.update_plot()

    def generate_am_signal(self, Ac, fc, Am, fm, t):
        baseband_signal = Ac * np.cos(2 * np.pi * fc * t)
        carrier_signal = Am * np.cos(2 * np.pi * fm * t)
        modulated_signal = (Ac + carrier_signal) * np.cos(2 * np.pi * fc * t)
        return baseband_signal, carrier_signal, modulated_signal

    def update_parameter(self, param_name, value):
        if param_name == "Amplituda nośnej":
            self.Ac = value
        elif param_name == "Częstotliwość nośnej":
            self.fc = value
        elif param_name == "Amplituda sygnału modulującego":
            self.Am = value
        elif param_name == "Częstotliwość sygnału modulującego":
            self.fm = value
        self.update_plot()

    def update_plot(self):
        self.axs[0].clear()
        self.axs[1].clear()
        self.axs[2].clear()
        
        baseband_signal, carrier_signal, modulated_signal = self.generate_am_signal(
            self.Ac, self.fc, self.Am, self.fm, self.t
        )
        
        self.axs[0].plot(self.t, baseband_signal, label="Baseband Signal (M(t))")
        self.axs[0].set_ylim(np.min(baseband_signal) - 0.5, np.max(baseband_signal) + 0.5)
        self.axs[0].set_title("Modulacja AM: Sygnał nośny, Sygnał modulujący, Sygnał zmodulowany")
        self.axs[0].grid()
        
        self.axs[1].plot(self.t, carrier_signal, label="Carrier Signal (C(t))", color='orange')
        self.axs[1].set_ylim(np.min(carrier_signal) - 0.5, np.max(carrier_signal) + 0.5)

        self.axs[1].grid()
        
        self.axs[2].plot(self.t, modulated_signal, label="AM Modulated Signal (S(t))", color='green')
        self.axs[2].set_ylim(np.min(modulated_signal) - 0.5, np.max(modulated_signal) + 0.5)

    
        self.axs[2].grid()
        
        self.fig.canvas.draw()

class AMDepthSimulation:
    def __init__(self):
        # Parametry początkowe
        self.mu = 0.5  # Głębokość modulacji
        self.Ac = 1.0  # Amplituda nośnej
        self.fc = 150.0  # Częstotliwość nośnej (na sztywno)
        self.fm = 10.0  # Częstotliwość sygnału modulującego (na sztywno)
        self.t = np.linspace(0, 1, 1000)

        # Tworzenie wykresu Matplotlib
        self.fig, self.axs = plt.subplots(3, 1, figsize=(6, 8), sharex=True)
        self.update_plot()

    def generate_am_signal_with_depth(self, mu, Ac, fc, fm, t):
        Am = mu * Ac  # Amplituda sygnału modulującego zależna od głębokości modulacji
        carrier_signal = Ac * np.cos(2 * np.pi * fc * t)
        modulating_signal = Am * np.cos(2 * np.pi * fm * t)
        modulated_signal = (Ac + modulating_signal) * np.cos(2 * np.pi * fc * t)
        return carrier_signal, modulating_signal, modulated_signal

    def update_parameter(self, param_name, value):
        if param_name == "Głębokość modulacji (μ)":
            self.mu = value
        self.update_plot()

    def update_plot(self):
        self.axs[0].clear()
        self.axs[1].clear()
        self.axs[2].clear()
        
        carrier_signal, modulating_signal, modulated_signal = self.generate_am_signal_with_depth(
            self.mu, self.Ac, self.fc, self.fm, self.t
        )
        
        self.axs[0].plot(self.t, carrier_signal, label="Carrier Signal (C(t))", color='orange')
        self.axs[0].set_title("Modulacja AM: Sygnał nośny, Sygnał modulujący, Sygnał zmodulowany")
        self.axs[0].set_ylabel("Amplitude")
        self.axs[0].grid()
        
        self.axs[1].plot(self.t, modulating_signal, label="Modulating Signal (M(t))", color='blue')
        self.axs[1].set_ylim(np.min(modulating_signal) - 0.5, np.max(modulating_signal) + 0.5)


        self.axs[1].set_ylabel("Amplitude")
        self.axs[1].grid()
        
        self.axs[2].plot(self.t, modulated_signal, label="AM Modulated Signal (S(t))", color='green')
        self.axs[2].set_xlabel("Time (s)")
        self.axs[2].set_ylabel("Amplitude")
        self.axs[2].grid()
        
        self.fig.canvas.draw()


class FMSim:
    def __init__(self):
        # Parametry początkowe
        self.Ac = 1.0  # Amplituda nośnej
        self.fc = 100.0  # Częstotliwość nośnej
        self.Am = 1.0  # Amplituda sygnału modulującego
        self.fm = 10.0  # Częstotliwość sygnału modulującego
        self.kf = 50.0  # Wrażliwość częstotliwości (przykładowa wartość)
        self.t = np.linspace(0, 1, 1000)

        # Tworzenie wykresu Matplotlib
        self.fig, self.axs = plt.subplots(3, 1, figsize=(6, 8), sharex=True)
        self.update_plot()

    def generate_fm_signal(self, Ac, fc, Am, fm, kf, t):
        beta = (kf * Am) / fm  # Obliczenie indeksu modulacji
        baseband_signal = Am * np.cos(2 * np.pi * fm * t)
        carrier_signal = Ac * np.cos(2 * np.pi * fc * t)
        modulated_signal = Ac * np.cos(2 * np.pi * fc * t + beta * np.sin(2 * np.pi * fm * t))
        return baseband_signal, carrier_signal, modulated_signal

    def update_parameter(self, param_name, value):
        if param_name == "Amplituda nośnej":
            self.Ac = value
        elif param_name == "Częstotliwość nośnej":
            self.fc = value
        elif param_name == "Amplituda sygnału modulującego":
            self.Am = value
        elif param_name == "Częstotliwość sygnału modulującego":
            self.fm = value
        self.update_plot()

    def update_plot(self):
        self.axs[0].clear()
        self.axs[1].clear()
        self.axs[2].clear()
        
        baseband_signal, carrier_signal, modulated_signal = self.generate_fm_signal(
            self.Ac, self.fc, self.Am, self.fm, self.kf, self.t
        )
        
        self.axs[0].plot(self.t, baseband_signal, label="Baseband Signal (M(t))")
        self.axs[0].set_ylim(np.min(baseband_signal) - 0.5, np.max(baseband_signal) + 0.5)
        self.axs[0].set_title("Modulacja FM: Sygnał nośny, Sygnał modulujący, Sygnał zmodulowany")
        self.axs[0].grid()
        
        self.axs[1].plot(self.t, carrier_signal, label="Carrier Signal (C(t))", color='orange')
        self.axs[1].set_ylim(np.min(carrier_signal) - 0.5, np.max(carrier_signal) + 0.5)
        self.axs[1].grid()
        
        self.axs[2].plot(self.t, modulated_signal, label="FM Modulated Signal (S(t))", color='green')
        self.axs[2].set_ylim(np.min(modulated_signal) - 0.5, np.max(modulated_signal) + 0.5)
        self.axs[2].grid()
        
        self.fig.canvas.draw()


SIMULATION_CLASSES = {
    "direct_detection": DirectDetectionSimulation,
    "coherent_detection": CoherentDetectionSimulation,
    "qam_simulation" : QAMSimulation,
    "am_simulation" : AMSimulation,
    "am_depth_simulation" : AMDepthSimulation,
    "fm_sim" : FMSim

}
