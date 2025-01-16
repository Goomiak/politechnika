import numpy as np
import matplotlib.pyplot as plt

# Parametry symulacji
M = 16  # Liczba symboli (np. 16-QAM)
N = 1000  # Liczba symboli do przesłania
Eb_N0_dB = 10  # Stosunek energii bitowej do szumu w dB

# Generowanie mapowania QAM
bits_per_symbol = int(np.log2(M))
symbol_map = np.arange(M)
real_parts = 2 * (symbol_map % np.sqrt(M)) - np.sqrt(M) + 1
imag_parts = 2 * (symbol_map // np.sqrt(M)) - np.sqrt(M) + 1
constellation = (real_parts + 1j * imag_parts) / np.sqrt(M)

# Normalizacja konstelacji
avg_symbol_power = np.mean(np.abs(constellation) ** 2)
constellation /= np.sqrt(avg_symbol_power)

# Generowanie danych wejściowych
bits = np.random.randint(0, 2, size=(N * bits_per_symbol))
symbol_indices = np.packbits(bits).astype(np.int16) % M
symbols = constellation[symbol_indices]

# Generowanie szumu
Eb_N0_linear = 10 ** (Eb_N0_dB / 10)
noise_variance = 1 / (2 * Eb_N0_linear)
noise = (np.random.normal(0, np.sqrt(noise_variance), N) + 
         1j * np.random.normal(0, np.sqrt(noise_variance), N))

# Sygnał odebrany (sygnał + szum)
received_symbols = symbols + noise

# Demodulacja QAM
recovered_indices = np.argmin(np.abs(received_symbols[:, np.newaxis] - constellation), axis=1)
recovered_bits = np.unpackbits(recovered_indices.astype(np.uint8))[:N * bits_per_symbol]

# Obliczanie liczby błędów
bit_errors = np.sum(bits != recovered_bits)
ber = bit_errors / len(bits)

# Wyniki symulacji
print(f"Liczba błędów bitowych: {bit_errors}")
print(f"BER (Bit Error Rate): {ber}")

# Wizualizacja wyników
plt.figure(figsize=(10, 6))

# Diagram konstelacji (odebrane symbole)
plt.scatter(received_symbols.real, received_symbols.imag, color='blue', alpha=0.5, label='Odebrane symbole')

# Diagram konstelacji (idealne symbole)
plt.scatter(constellation.real, constellation.imag, color='red', label='Idealne symbole', marker='x')

plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.title(f"Diagram konstelacji dla {M}-QAM (Eb/N0 = {Eb_N0_dB} dB)")
plt.xlabel("Część rzeczywista")
plt.ylabel("Część urojona")
plt.show()
