import numpy as np
import matplotlib.pyplot as plt

# Stałe
c = 3e8  # Prędkość światła w próżni [m/s]
f_signal = 1e9  # Częstotliwość sygnału optycznego [Hz]
f_LO = 1e9 + 1e6  # Częstotliwość lokalnego oscylatora [Hz]
amplitude_signal = 1.0  # Amplituda sygnału
amplitude_LO = 1.0  # Amplituda lokalnego oscylatora
phi_signal = np.pi / 4  # Faza sygnału [rad]
phi_LO = 0  # Faza lokalnego oscylatora [rad]
t = np.linspace(0, 1e-6, 1000)  # Próbki czasu [s]

# Sygnał optyczny
signal = amplitude_signal * np.cos(2 * np.pi * f_signal * t + phi_signal)

# Detekcja bezpośrednia (moc sygnału)
detected_power = signal**2

# Wizualizacja
plt.figure(figsize=(10, 6))
plt.plot(t, signal, label="Sygnał optyczny")
plt.plot(t, detected_power, label="Moc sygnału (detekcja bezpośrednia)")
plt.xlabel("Czas [s]")
plt.ylabel("Amplituda")
plt.title("Detekcja bezpośrednia")
plt.legend()
plt.grid()
plt.show()
