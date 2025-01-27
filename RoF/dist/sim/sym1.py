import numpy as np
import matplotlib.pyplot as plt

# Parametry symulacji
P_min = 0.0  # minimalna moc lasera [W]
P_max = 10e-3  # maksymalna moc lasera [W]
P_points = 100  # liczba punktów symulacji
S = 0.6  # czułość fotodiody [A/W]
R_f = 1e6  # rezystancja wzmacniacza transimpedancyjnego [ohm]

# Generowanie danych
P_values = np.linspace(P_min, P_max, P_points)  # Wartości mocy lasera
I_values = S * P_values  # Prąd fotodiody [A]
V_values = I_values * R_f  # Napięcie wyjściowe wzmacniacza [V]

# Tworzenie wykresów
plt.figure(figsize=(12, 6))

# Wykres 1: Prąd fotodiody vs Moc lasera
plt.subplot(1, 2, 1)
plt.plot(P_values * 1e3, I_values * 1e6, label="Czułość = {:.2f} A/W".format(S), color="blue")
plt.xlabel("Moc lasera [mW]")
plt.ylabel("Prąd fotodiody [uA]")
plt.title("Prąd fotodiody vs Moc lasera")
plt.grid(True)
plt.legend()

# Wykres 2: Napięcie wyjściowe vs Prąd fotodiody
plt.subplot(1, 2, 2)
plt.plot(I_values * 1e6, V_values, label="R_f = {:.1e} Ohm".format(R_f), color="green")
plt.xlabel("Prąd fotodiody [uA]")
plt.ylabel("Napięcie wyjściowe [V]")
plt.title("Napięcie wyjściowe vs Prąd fotodiody")
plt.grid(True)
plt.legend()

# Wyświetlenie wykresów
plt.tight_layout()
plt.show()
