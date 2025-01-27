import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Parametry sygnału
fs = 1000  # Częstotliwość próbkowania (Hz)
t = np.linspace(0, 1, fs)  # Oś czasu (1 sekunda)
f_carrier = 50  # Częstotliwość nośna (Hz)
f_mod = 5  # Częstotliwość modulacji (Hz)
amplitude = 1  # Amplituda sygnału
responsivity = 0.5  # Responsywność fotodetektora (R)

# Sygnał optyczny E(t)
E_t = amplitude * (1 + 0.5 * np.sin(2 * np.pi * f_mod * t)) * np.sin(2 * np.pi * f_carrier * t)

# Moc optyczna P(t)
P_t = np.abs(E_t)**2

# Prąd fotodetektora I(t)
I_t = responsivity * P_t

# Filtracja sygnału (filtr dolnoprzepustowy RC)
def lowpass_filter(data, cutoff, fs, order=2):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

cutoff_freq = 20  # Częstotliwość odcięcia filtra (Hz)
I_t_filtered = lowpass_filter(I_t, cutoff_freq, fs)

# Wizualizacja
plt.figure(figsize=(12, 8))

# Sygnał optyczny
plt.subplot(3, 1, 1)
plt.plot(t, E_t, label='E(t) - Sygnał optyczny')
plt.title('Sygnał optyczny E(t)')
plt.xlabel('Czas (s)')
plt.ylabel('Amplituda')
plt.legend()
plt.grid()

# Moc optyczna
plt.subplot(3, 1, 2)
plt.plot(t, P_t, label='P(t) - Moc optyczna', color='orange')
plt.title('Moc optyczna P(t)')
plt.xlabel('Czas (s)')
plt.ylabel('Moc')
plt.legend()
plt.grid()

# Prąd fotodetektora
plt.subplot(3, 1, 3)
plt.plot(t, I_t, label='I(t) - Prąd fotodetektora (bez filtra)', color='red', alpha=0.7)
plt.plot(t, I_t_filtered, label='I(t) - Prąd fotodetektora (po filtrze)', color='green')
plt.title('Prąd fotodetektora I(t)')
plt.xlabel('Czas (s)')
plt.ylabel('Prąd')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
