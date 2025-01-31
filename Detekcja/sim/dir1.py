import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import Qt

class SimulationWidget(QWidget):
    def __init__(self):
        super().__init__()

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

        # Tworzymy figurę Matplotlib jako widżet
        self.figure, self.axs = plt.subplots(3, 1, figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)
        self.plot_signals()

        # Layout dla PySide6
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        # Suwaki PySide6 (zamiast matplotlib.widgets.Slider)
        self.amp_slider = self.create_slider("Amplituda", 0.1, 2.0, self.amplitude, self.update_amplitude)
        self.freq_slider = self.create_slider("Częstotliwość [THz]", 10, 200, self.f_carrier, self.update_frequency)
        self.time_slider = self.create_slider("Podstawa czasu [ps]", 0.1, 2.0, self.time_base, self.update_time)

        layout.addWidget(self.amp_slider)
        layout.addWidget(self.freq_slider)
        layout.addWidget(self.time_slider)

        self.setLayout(layout)

    def create_slider(self, label_text, min_val, max_val, initial_value, callback):
        """Tworzy suwak z etykietą"""
        slider_widget = QWidget()
        slider_layout = QVBoxLayout()

        label = QLabel(f"{label_text}: {initial_value:.2f}")
        slider_layout.addWidget(label)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(int(min_val * 100))
        slider.setMaximum(int(max_val * 100))
        slider.setValue(int(initial_value * 100))
        slider.valueChanged.connect(lambda value: callback(value / 100, label))

        slider_layout.addWidget(slider)
        slider_widget.setLayout(slider_layout)

        return slider_widget

    def update_amplitude(self, value, label):
        """Aktualizuje amplitudę i rysuje ponownie"""
        self.amplitude = value
        label.setText(f"Amplituda: {value:.2f}")
        self.update_plot()

    def update_frequency(self, value, label):
        """Aktualizuje częstotliwość i rysuje ponownie"""
        self.f_carrier = value
        label.setText(f"Częstotliwość [THz]: {value:.2f}")
        self.update_plot()

    def update_time(self, value, label):
        """Aktualizuje zakres czasu i rysuje ponownie"""
        self.time_base = value
        label.setText(f"Podstawa czasu [ps]: {value:.2f}")
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
        """Tworzy wykresy początkowe"""
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

        self.canvas.draw()

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

        self.canvas.draw()