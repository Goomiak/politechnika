import numpy as np
import matplotlib.pyplot as plt
import gradio as gr

def coherent_simulation(freq_carrier, freq_lo, phase_shift):
    # Parametry początkowe
    laser_power_carrier = 10e-3  # W
    laser_power_lo = 1e-3        # W
    sampling_rate = 1e8          # Hz
    time = np.arange(0, 1e-5, 1/sampling_rate)
    
    amplitude_carrier = np.sqrt(2 * laser_power_carrier)
    amplitude_lo = np.sqrt(2 * laser_power_lo)
    
    # Sygnały
    carrier_signal = amplitude_carrier * np.cos(2 * np.pi * freq_carrier * time)
    lo_signal = amplitude_lo * np.cos(2 * np.pi * freq_lo * time + phase_shift)
    interference_signal = carrier_signal * lo_signal
    interference_dc = np.mean(interference_signal)
    
    # Wykres
    fig, axs = plt.subplots(3, 1, figsize=(10, 8))
    
    axs[0].plot(time, carrier_signal, label="Sygnał nośny")
    axs[0].set_title("Sygnał nośny")
    axs[0].legend()
    
    axs[1].plot(time, lo_signal, label="Lokalny oscylator", color='orange')
    axs[1].set_title("Lokalny oscylator")
    axs[1].legend()
    
    axs[2].plot(time, interference_signal, label="Sygnał po detekcji", color='green')
    axs[2].axhline(y=interference_dc, color='red', linestyle='--', label=f"DC = {interference_dc:.2e} W")
    axs[2].set_title("Sygnał po detekcji koherentnej")
    axs[2].legend()
    
    plt.tight_layout()
    plt.close(fig)
    return fig

interface = gr.Interface(
    fn=coherent_simulation,
    inputs=[
        gr.Slider(1e5, 5e6, step=1e5, label="Częstotliwość nośnej [Hz]"),
        gr.Slider(1e5, 5e6, step=1e5, label="Częstotliwość oscylatora [Hz]"),
        gr.Slider(0, 2 * np.pi, step=0.1, label="Faza [rad]")
    ],
    outputs="plot",
    live_update=True  # Umożliwia odświeżanie na bieżąco
)

interface.launch()