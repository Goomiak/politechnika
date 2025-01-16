import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Funkcja do generowania sygnału modulowanego
def plot_am_modulation(carrier_freq=10, carrier_ampl=1, mod_freq=2, mod_ampl=0.5):
    t = np.linspace(0, 1, 1000)  # 1 sekunda czasu, 1000 próbek

    # Tworzenie wykresów
    fig, ax = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)

    # Sygnały początkowe
    carrier = carrier_ampl * np.sin(2 * np.pi * carrier_freq * t)
    mod_signal = mod_ampl * np.sin(2 * np.pi * mod_freq * t)
    modulated_signal = (1 + mod_signal) * carrier

    # Ustawienia subplotów
    ax[0, 0].set_title("Sygnał nośny")
    ax[0, 0].set_xlabel("Czas [s]")
    ax[0, 0].set_ylabel("Amplituda")
    carrier_line, = ax[0, 0].plot(t, carrier, label="Sygnał nośny")
    ax[0, 0].grid(True)
    ax[0, 0].legend()

    ax[0, 1].set_title("Sygnał modulujący")
    ax[0, 1].set_xlabel("Czas [s]")
    ax[0, 1].set_ylabel("Amplituda")
    mod_signal_line, = ax[0, 1].plot(t, mod_signal, color='orange', label="Sygnał modulujący")
    ax[0, 1].grid(True)
    ax[0, 1].legend()

    ax[1, 0].set_title("Sygnał modulowany (AM)")
    ax[1, 0].set_xlabel("Czas [s]")
    ax[1, 0].set_ylabel("Amplituda")
    modulated_line, = ax[1, 0].plot(t, modulated_signal, color='green', label="Sygnał modulowany (AM)")
    ax[1, 0].grid(True)
    ax[1, 0].legend()

    # Wyłączenie niewykorzystanego wykresu
    ax[1, 1].axis('off')

    # Suwaki obok wykresu sygnału modulowanego, wyśrodkowane w swojej ćwiartce
    slider_ax1 = plt.axes([0.6, 0.12, 0.3, 0.03])
    slider_ax2 = plt.axes([0.6, 0.17, 0.3, 0.03])
    slider_ax3 = plt.axes([0.6, 0.22, 0.3, 0.03])
    slider_ax4 = plt.axes([0.6, 0.27, 0.3, 0.03])

    carrier_freq_slider = Slider(slider_ax1, 'F. nośna [Hz]', 1, 50, valinit=carrier_freq)
    carrier_ampl_slider = Slider(slider_ax2, 'A. nośna', 0.1, 2, valinit=carrier_ampl)
    mod_freq_slider = Slider(slider_ax3, 'F. modulacji [Hz]', 0.1, 10, valinit=mod_freq)
    mod_ampl_slider = Slider(slider_ax4, 'A. modulacji', 0, 1, valinit=mod_ampl)

    # Aktualizacja sygnałów
    def update(val):
        carrier_freq = carrier_freq_slider.val
        carrier_ampl = carrier_ampl_slider.val
        mod_freq = mod_freq_slider.val
        mod_ampl = mod_ampl_slider.val

        carrier = carrier_ampl * np.sin(2 * np.pi * carrier_freq * t)
        mod_signal = mod_ampl * np.sin(2 * np.pi * mod_freq * t)
        modulated_signal = (1 + mod_signal) * carrier

        carrier_line.set_ydata(carrier)
        mod_signal_line.set_ydata(mod_signal)
        modulated_line.set_ydata(modulated_signal)

        fig.canvas.draw_idle()

    carrier_freq_slider.on_changed(update)
    carrier_ampl_slider.on_changed(update)
    mod_freq_slider.on_changed(update)
    mod_ampl_slider.on_changed(update)

    plt.show()

# Uruchomienie aplikacji
plot_am_modulation()
