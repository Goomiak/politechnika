import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
from matplotlib.widgets import Slider

# Parametry symulacji
t = np.linspace(0, 1, 1000)  # czas (1s, 1000 próbek)

# Funkcja do aktualizacji wykresów
def update(val):
    intensity_factor = slider_intensity.val
    input_light_intensity = intensity_factor * (0.5 + 0.5 * np.sin(2 * np.pi * 10 * t))

    # 1. Fotodioda - generacja prądu proporcjonalnego do intensywności światła
    responsivity = 0.6  # czułość fotodiody (A/W)
    photo_current = responsivity * input_light_intensity

    # 2. Wzmacniacz transimpedancyjny (TIA)
    transimpedance_gain = 1e4  # wzmocnienie (Ohm)
    tia_output_voltage = photo_current * transimpedance_gain

    # 3. Filtr dolnoprzepustowy RC
    cutoff_frequency = 20  # częstotliwość odcięcia filtra w Hz
    rc = 1 / (2 * np.pi * cutoff_frequency)
    b, a = [1], [rc, 1]  # współczynniki filtra RC
    filtered_signal = lfilter(b, a, tia_output_voltage)

    # Aktualizacja wykresów
    ax1.clear()
    ax1.plot(t, input_light_intensity, label="Intensywność światła")
    ax1.set_title("1. Intensywność światła (wejście)")
    ax1.set_xlabel("Czas [s]")
    ax1.set_ylabel("Intensywność")
    ax1.grid(True)
    ax1.legend()

    ax2.clear()
    ax2.plot(t, tia_output_voltage, label="Napięcie wyjściowe TIA", color="orange")
    ax2.set_title("2. Wzmacniacz transimpedancyjny (TIA)")
    ax2.set_xlabel("Czas [s]")
    ax2.set_ylabel("Napięcie [V]")
    ax2.grid(True)
    ax2.legend()

    ax3.clear()
    ax3.plot(t, filtered_signal, label="Sygnał po filtrze RC", color="green")
    ax3.set_title("3. Filtr dolnoprzepustowy RC")
    ax3.set_xlabel("Czas [s]")
    ax3.set_ylabel("Napięcie [V]")
    ax3.grid(True)
    ax3.legend()

    fig.canvas.draw_idle()

# Początkowe wartości intensywności światła
initial_intensity = 1.0
input_light_intensity = initial_intensity * (0.5 + 0.5 * np.sin(2 * np.pi * 10 * t))

# 1. Fotodioda - generacja prądu proporcjonalnego do intensywności światła
responsivity = 0.6  # czułość fotodiody (A/W)
photo_current = responsivity * input_light_intensity

# 2. Wzmacniacz transimpedancyjny (TIA)
transimpedance_gain = 1e4  # wzmocnienie (Ohm)
tia_output_voltage = photo_current * transimpedance_gain

# 3. Filtr dolnoprzepustowy RC
cutoff_frequency = 20  # częstotliwość odcięcia filtra w Hz
rc = 1 / (2 * np.pi * cutoff_frequency)
b, a = [1], [rc, 1]  # współczynniki filtra RC
filtered_signal = lfilter(b, a, tia_output_voltage)

# Wykresy
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)

# 1. Intensywność światła
ax1.plot(t, input_light_intensity, label="Intensywność światła")
ax1.set_title("1. Intensywność światła (wejście)")
ax1.set_xlabel("Czas [s]")
ax1.set_ylabel("Intensywność")
ax1.grid(True)
ax1.legend()

# 2. Napięcie wyjściowe TIA
ax2.plot(t, tia_output_voltage, label="Napięcie wyjściowe TIA", color="orange")
ax2.set_title("2. Wzmacniacz transimpedancyjny (TIA)")
ax2.set_xlabel("Czas [s]")
ax2.set_ylabel("Napięcie [V]")
ax2.grid(True)
ax2.legend()

# 3. Filtr RC
ax3.plot(t, filtered_signal, label="Sygnał po filtrze RC", color="green")
ax3.set_title("3. Filtr dolnoprzepustowy RC")
ax3.set_xlabel("Czas [s]")
ax3.set_ylabel("Napięcie [V]")
ax3.grid(True)
ax3.legend()

# Dodanie suwaka do regulacji intensywności światła
ax_slider = plt.axes([0.25, 0.01, 0.5, 0.02], facecolor='lightgoldenrodyellow')
slider_intensity = Slider(ax_slider, 'Intensywność', 0.1, 2.0, valinit=initial_intensity)
slider_intensity.on_changed(update)

plt.show()
