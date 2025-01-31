import numpy as np
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
    amplitude = amp_slider.val
    frequency = freq_slider.val

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
    fig.canvas.draw_idle()

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

# Tworzenie wykresów
fig, axs = plt.subplots(3, 1, figsize=(10, 8))
plt.subplots_adjust(bottom=0.25)

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

# Dodanie suwaków
axcolor = 'lightgoldenrodyellow'
amp_slider_ax = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
freq_slider_ax = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor=axcolor)

amp_slider = Slider(amp_slider_ax, 'Amplituda', 0.1, 2.0, valinit=amplitude)
freq_slider = Slider(freq_slider_ax, 'Częstotliwość', 10, 100, valinit=f_carrier)

# Podpięcie suwaków do funkcji aktualizującej
amp_slider.on_changed(update)
freq_slider.on_changed(update)

plt.show()
