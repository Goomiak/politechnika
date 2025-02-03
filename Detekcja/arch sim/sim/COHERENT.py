import numpy as np
import matplotlib.pyplot as plt

# Założenia
laser_power_carrier = 10e-3  # moc lasera nośnego [W]
laser_power_lo = 1e-3        # moc lokalnego oscylatora [W]
frequency = 1e6             # częstotliwość fali [Hz]
phase_shift = np.pi / 4     # różnica faz [rad]
sampling_rate = 1e8         # częstotliwość próbkowania [Hz]
time = np.arange(0, 1e-5, 1/sampling_rate)  # czas [s]

# Obliczenia amplitud
amplitude_carrier = np.sqrt(2 * laser_power_carrier)
amplitude_lo = np.sqrt(2 * laser_power_lo)

# Generacja sygnałów
carrier_signal = amplitude_carrier * np.cos(2 * np.pi * frequency * time)
lo_signal = amplitude_lo * np.cos(2 * np.pi * frequency * time + phase_shift)

# Detekcja koherentna (interferencja)
interference_signal = carrier_signal * lo_signal

# Wyekstrahowanie sygnału detekcji (po filtracji dolnoprzepustowej)
interference_dc = np.mean(interference_signal)



# Wizualizacja
plt.figure(figsize=(12, 8))

# Nośna
plt.subplot(3, 1, 1)
plt.plot(time, carrier_signal, label="Sygnał nośny")
plt.title("Sygnał nośny")
plt.xlabel("Czas [s]")
plt.ylabel("Amplituda")
plt.grid()
plt.legend()

# Lokalny oscylator
plt.subplot(3, 1, 2)
plt.plot(time, lo_signal, label="Lokalny oscylator", color='orange')
plt.title("Lokalny oscylator")
plt.xlabel("Czas [s]")
plt.ylabel("Amplituda")
plt.grid()
plt.legend()

# Interferencja
plt.subplot(3, 1, 3)
plt.plot(time, interference_signal, label="Sygnał po detekcji koherentnej", color='green')
plt.axhline(interference_dc, color='red', linestyle='--', label=f"Składowa DC = {interference_dc:.2e} W")
plt.title("Sygnał po detekcji koherentnej")
plt.xlabel("Czas [s]")
plt.ylabel("Amplituda")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
