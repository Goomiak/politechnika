import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Function to generate AM modulated signal with modulation depth
def generate_am_signal_with_depth(mu, Ac, fc, fm, t):
    Am = mu * Ac  # Amplitude of the modulating signal based on modulation depth
    carrier_signal = Ac * np.cos(2 * np.pi * fc * t)
    modulating_signal = Am * np.cos(2 * np.pi * fm * t)
    modulated_signal = (Ac + modulating_signal) * np.cos(2 * np.pi * fc * t)
    return carrier_signal, modulating_signal, modulated_signal

# Time vector
t = np.linspace(0, 1, 1000)

# Initial parameters
mu_init = 0.5  # Modulation depth
Ac_init = 1.0  # Carrier amplitude
fc_init = 5.0  # Carrier frequency
fm_init = 100.0  # Modulating signal frequency

# Generate initial signals
carrier_signal, modulating_signal, modulated_signal = generate_am_signal_with_depth(mu_init, Ac_init, fc_init, fm_init, t)

# Create the figure and axes
fig, axs = plt.subplots(3, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [0.5, 0.5, 1]})
plt.subplots_adjust(left=0.1, bottom=0.3, hspace=0.6)

# Plot carrier signal
line_carrier, = axs[0].plot(t, carrier_signal, label="Carrier Signal (C(t))", color='orange')
axs[0].set_title("Carrier Signal (C(t))")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Amplitude")
axs[0].grid()

# Plot modulating signal
line_modulating, = axs[1].plot(t, modulating_signal, label="Modulating Signal (M(t))", color='blue')
axs[1].set_title("Modulating Signal (M(t))")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Amplitude")
axs[1].grid()

# Plot modulated signal
line_modulated, = axs[2].plot(t, modulated_signal, label="AM Modulated Signal (S(t))", color='green')
axs[2].set_title("AM Modulated Signal (S(t))")
axs[2].set_xlabel("Time (s)")
axs[2].set_ylabel("Amplitude")
axs[2].grid()

# Add sliders for parameters
axcolor = 'lightgoldenrodyellow'
ax_mu = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_fc = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_fm = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)

slider_mu = Slider(ax_mu, 'Modulation Depth (μ)', 0.0, 1.0, valinit=mu_init)
slider_fc = Slider(ax_fc, 'Carrier Frequency (fc)', 1.0, 10.0, valinit=fc_init)
slider_fm = Slider(ax_fm, 'Modulating Frequency (fm)', 0.1, 200.0, valinit=fm_init)

# Update function with auto-rescaling of y-axis
def update(val):
    mu = slider_mu.val
    fc = slider_fc.val
    fm = slider_fm.val
    carrier_signal, modulating_signal, modulated_signal = generate_am_signal_with_depth(mu, Ac_init, fc, fm, t)
    line_carrier.set_ydata(carrier_signal)
    line_modulating.set_ydata(modulating_signal)
    line_modulated.set_ydata(modulated_signal)
    axs[0].set_ylim(carrier_signal.min() - 0.5, carrier_signal.max() + 0.5)
    axs[1].set_ylim(modulating_signal.min() - 0.5, modulating_signal.max() + 0.5)
    axs[2].set_ylim(modulated_signal.min() - 0.5, modulated_signal.max() + 0.5)
    fig.canvas.draw_idle()

# Connect sliders to update function
slider_mu.on_changed(update)
slider_fc.on_changed(update)
slider_fm.on_changed(update)

plt.show()
