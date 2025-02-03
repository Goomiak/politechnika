import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def coherent_detection_simulation():
    # Parametry początkowe
    fs = 1e9  # Częstotliwość próbkowania (1 GHz)
    t = np.linspace(0, 1e-6, int(fs * 1e-6))  # Oś czasu (1 us)
    f_signal = 100e6  # Częstotliwość sygnału optycznego (100 MHz)
    f_lo = 100e6  # Częstotliwość lokalnego oscylatora (100 MHz)
    noise_level = 0.1  # Poziom szumu

    # Funkcja aktualizacji
    def update(val):
        nonlocal f_signal, f_lo
        f_signal = slider_signal.val * 1e6
        f_lo = slider_lo.val * 1e6

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

        # Aktualizacja wykresów
        ax1.clear()
        ax2.clear()
        ax3.clear()

        ax1.plot(t, optical_signal)
        ax1.set_title("Sygnał optyczny")
        ax1.set_xlabel("Czas [s]")
        ax1.set_ylabel("Amplituda")

        ax2.plot(t, lo_signal)
        ax2.set_title("Sygnał lokalnego oscylatora (LO)")
        ax2.set_xlabel("Czas [s]")
        ax2.set_ylabel("Amplituda")

        ax3.plot(t, dsp_signal)
        ax3.set_title("Sygnał po DSP")
        ax3.set_xlabel("Czas [s]")
        ax3.set_ylabel("Amplituda")

        plt.draw()

    # Tworzenie wykresów
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6), constrained_layout=True)

    # Inicjalizacja suwaków
    ax_slider_signal = plt.axes([0.2, 0.01, 0.65, 0.03])
    ax_slider_lo = plt.axes([0.2, 0.05, 0.65, 0.03])

    slider_signal = Slider(ax_slider_signal, 'F. Sygnału [MHz]', 50, 200, valinit=f_signal / 1e6)
    slider_lo = Slider(ax_slider_lo, 'F. LO [MHz]', 50, 200, valinit=f_lo / 1e6)

    slider_signal.on_changed(update)
    slider_lo.on_changed(update)

    # Pierwsze wywołanie aktualizacji
    update(None)

    plt.show()

# Uruchomienie symulacji
coherent_detection_simulation()
