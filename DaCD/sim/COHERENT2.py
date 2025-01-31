import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Założenia początkowe
laser_power_carrier = 10e-3  # moc lasera nośnego [W]
laser_power_lo = 1e-3        # moc lokalnego oscylatora [W]
freq_carrier = 1e6          # początkowa częstotliwość nośnej [Hz]
freq_lo = 1e6               # początkowa częstotliwość lokalnego oscylatora [Hz]
phase_shift = np.pi / 4     # początkowa różnica faz [rad]
sampling_rate = 1e8         # częstotliwość próbkowania [Hz]
time = np.arange(0, 1e-5, 1/sampling_rate)  # czas [s]

# Obliczenia amplitud
amplitude_carrier = np.sqrt(2 * laser_power_carrier)
amplitude_lo = np.sqrt(2 * laser_power_lo)

# Funkcja aktualizująca sygnały
def update(val):
    freq_carrier = carrier_slider.val
    freq_lo = lo_slider.val
    phase = phase_slider.val

    # Aktualizacja sygnałów
    carrier_signal = amplitude_carrier * np.cos(2 * np.pi * freq_carrier * time)
    lo_signal = amplitude_lo * np.cos(2 * np.pi * freq_lo * time + phase)
    interference_signal = carrier_signal * lo_signal
    interference_dc = np.mean(interference_signal)

    # Aktualizacja wykresów
    line_carrier.set_ydata(carrier_signal)
    line_lo.set_ydata(lo_signal)
    line_interference.set_ydata(interference_signal)
    dc_line.set_ydata([interference_dc] * len(time))


    # Odświeżenie wykresów
    fig.canvas.draw_idle()

# Tworzenie figury
fig, axs = plt.subplots(3, 1, figsize=(12, 8))
plt.subplots_adjust(bottom=0.35)  # miejsce na suwaki

# Generacja sygnałów początkowych
carrier_signal = amplitude_carrier * np.cos(2 * np.pi * freq_carrier * time)
lo_signal = amplitude_lo * np.cos(2 * np.pi * freq_lo * time + phase_shift)
interference_signal = carrier_signal * lo_signal
interference_dc = np.mean(interference_signal)

# Wykresy
axs[0].set_title("Sygnał nośny")
line_carrier, = axs[0].plot(time, carrier_signal, label="Sygnał nośny")
axs[0].set_xlabel("Czas [s]")
axs[0].set_ylabel("Amplituda")
axs[0].grid()
axs[0].legend()

axs[1].set_title("Lokalny oscylator")
line_lo, = axs[1].plot(time, lo_signal, label="Lokalny oscylator", color='orange')
axs[1].set_xlabel("Czas [s]")
axs[1].set_ylabel("Amplituda")
axs[1].grid()
axs[1].legend()

axs[2].set_title("Sygnał po detekcji koherentnej")
line_interference, = axs[2].plot(time, interference_signal, label="Sygnał po detekcji", color='green')
dc_line, = axs[2].plot(time, [interference_dc] * len(time), color='red', linestyle='--', label=f"Składowa DC = {interference_dc:.2e} W")
axs[2].set_xlabel("Czas [s]")
axs[2].set_ylabel("Amplituda")
axs[2].grid()
axs[2].legend()

# Dodanie suwaków
axcolor = 'lightgoldenrodyellow'
carrier_slider_ax = plt.axes([0.2, 0.25, 0.65, 0.03], facecolor=axcolor)
lo_slider_ax = plt.axes([0.2, 0.2, 0.65, 0.03], facecolor=axcolor)
phase_slider_ax = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor=axcolor)

carrier_slider = Slider(carrier_slider_ax, 'Częstotliwość nośnej [Hz]', 1e5, 5e6, valinit=freq_carrier, valstep=1e5)
lo_slider = Slider(lo_slider_ax, 'Częstotliwość oscylatora [Hz]', 1e5, 5e6, valinit=freq_lo, valstep=1e5)
phase_slider = Slider(phase_slider_ax, 'Faza [rad]', 0, 2 * np.pi, valinit=phase_shift)

# Podpięcie suwaków do funkcji aktualizującej
carrier_slider.on_changed(update)
lo_slider.on_changed(update)
phase_slider.on_changed(update)

plt.show()