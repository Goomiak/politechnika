import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.signal import butter, filtfilt

# Funkcja filtra dolnoprzepustowego RC
def lowpass_filter(data, cutoff, fs, order=2):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# Funkcja do aktualizacji wykresów
def update(val):
    amplitude = amp_slider.get()
    frequency = freq_slider.get()

    # Aktualizacja sygnału optycznego
    E_t = amplitude * (1 + 0.5 * np.sin(2 * np.pi * f_mod * t)) * np.sin(2 * np.pi * frequency * t)
    P_t = np.abs(E_t)**2  # Moc optyczna
    I_t = responsivity * P_t  # Prąd fotodetektora
    I_t_filtered = lowpass_filter(I_t, cutoff_freq, fs)  # Po filtrze

    # Aktualizacja danych na wykresach
    line_E.set_ydata(E_t)
    line_P.set_ydata(P_t)
    line_I_raw.set_ydata(I_t)
    line_I_filtered.set_ydata(I_t_filtered)

    # Odświeżenie wykresów
    canvas.draw()

# Parametry początkowe
fs = 1000  # Częstotliwość próbkowania (Hz)
t = np.linspace(0, 1, fs)  # Oś czasu (1 sekunda)
f_carrier = 50  # Początkowa częstotliwość nośna (Hz)
f_mod = 5  # Częstotliwość modulacji (Hz)
amplitude = 1  # Początkowa amplituda
responsivity = 0.5  # Responsywność fotodetektora (R)
cutoff_freq = 20  # Częstotliwość odcięcia filtra (Hz)

# Początkowy sygnał
E_t = amplitude * (1 + 0.5 * np.sin(2 * np.pi * f_mod * t)) * np.sin(2 * np.pi * f_carrier * t)
P_t = np.abs(E_t)**2
I_t = responsivity * P_t
I_t_filtered = lowpass_filter(I_t, cutoff_freq, fs)

# Tworzenie głównego okna Tkinter
root = tk.Tk()
root.title("Wykres w Tkinter")
root.geometry("1200x800")

# Tworzenie wykresów
fig, axs = plt.subplots(3, 1, figsize=(8, 6))
plt.subplots_adjust(hspace=0.5)

# Wykres E(t)
axs[0].set_title('Sygnał optyczny E(t)')
line_E, = axs[0].plot(t, E_t, label='E(t)')
axs[0].legend()
axs[0].grid()

# Wykres P(t)
axs[1].set_title('Moc optyczna P(t)')
line_P, = axs[1].plot(t, P_t, label='P(t)', color='orange')
axs[1].legend()
axs[1].grid()

# Wykres I(t)
axs[2].set_title('Prąd fotodetektora I(t)')
line_I_raw, = axs[2].plot(t, I_t, label='I(t) - bez filtra', color='red', alpha=0.7)
line_I_filtered, = axs[2].plot(t, I_t_filtered, label='I(t) - po filtrze', color='green')
axs[2].legend()
axs[2].grid()

# Osadzanie wykresu w oknie Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Suwaki
slider_frame = ttk.Frame(root)
slider_frame.pack(side=tk.BOTTOM, fill=tk.X)

amp_slider_label = ttk.Label(slider_frame, text="Amplituda:")
amp_slider_label.pack(side=tk.LEFT, padx=5)
amp_slider = ttk.Scale(slider_frame, from_=0.1, to=2.0, value=amplitude, orient=tk.HORIZONTAL, command=lambda val: update(val))
amp_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

freq_slider_label = ttk.Label(slider_frame, text="Częstotliwość:")
freq_slider_label.pack(side=tk.LEFT, padx=5)
freq_slider = ttk.Scale(slider_frame, from_=10, to=100, value=f_carrier, orient=tk.HORIZONTAL, command=lambda val: update(val))
freq_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

# Przycisk zamknięcia
close_button = ttk.Button(slider_frame, text="Zamknij", command=root.destroy)
close_button.pack(side=tk.RIGHT, padx=5)

# Uruchomienie aplikacji Tkinter
root.mainloop()
