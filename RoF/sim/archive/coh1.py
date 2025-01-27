import numpy as np
import matplotlib.pyplot as plt

def coherent_detection_simulation():
    # Parametry
    fs = 1e9  # Częstotliwość próbkowania (1 GHz)
    t = np.linspace(0, 1e-6, int(fs * 1e-6))  # Oś czasu (1 us)
    f_signal = 100e6  # Częstotliwość sygnału optycznego (100 MHz)
    f_lo = 100e6  # Częstotliwość lokalnego oscylatora (100 MHz)
    noise_level = 0.1  # Poziom szumu

    # Generowanie sygnałów
    optical_signal = np.sin(2 * np.pi * f_signal * t)  # Sygnał optyczny
    lo_signal = np.sin(2 * np.pi * f_lo * t)  # Sygnał lokalnego oscylatora (LO)

    # Interferencja (sprzęgacz optyczny)
    interfered_signal = optical_signal * lo_signal

    # Dodanie szumu
    noisy_signal = interfered_signal + noise_level * np.random.normal(size=len(t))

    # Detekcja w fotodiodzie (kwadrat amplitudy)
    detected_signal = noisy_signal ** 2

    # Przetwarzanie analogowe (TIA + LPF)
    # TIA - wzmocnienie
    tia_signal = detected_signal * 10  # Wzmocnienie x10

    # LPF - filtr dolnoprzepustowy (używamy średniej ruchomej)
    def low_pass_filter(signal, window_size=50):
        return np.convolve(signal, np.ones(window_size)/window_size, mode='same')

    lpf_signal = low_pass_filter(tia_signal)

    # DSP - demodulacja i analiza fazy (dla uproszczenia normalizacja)
    dsp_signal = lpf_signal / np.max(np.abs(lpf_signal))

    # Wizualizacja
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 2, 1)
    plt.plot(t, optical_signal)
    plt.title("Sygnał optyczny")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")

    plt.subplot(3, 2, 2)
    plt.plot(t, lo_signal)
    plt.title("Sygnał lokalnego oscylatora (LO)")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")

    plt.subplot(3, 2, 3)
    plt.plot(t, interfered_signal)
    plt.title("Sygnał po interferencji")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")

    plt.subplot(3, 2, 4)
    plt.plot(t, noisy_signal)
    plt.title("Sygnał po dodaniu szumu")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")

    plt.subplot(3, 2, 5)
    plt.plot(t, lpf_signal)
    plt.title("Sygnał po filtrze dolnoprzepustowym")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")

    plt.subplot(3, 2, 6)
    plt.plot(t, dsp_signal)
    plt.title("Sygnał po DSP")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")

    plt.tight_layout()
    plt.show()

# Uruchomienie symulacji
coherent_detection_simulation()
