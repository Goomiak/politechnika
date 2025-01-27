import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Function to generate AM modulated signal
def generate_am_signal(Ac, fc, Am, fm, t):
    baseband_signal = Ac * np.cos(2 * np.pi * fc * t)
    carrier_signal = Am * np.cos(2 * np.pi * fm * t)
    modulated_signal = (Ac + carrier_signal) * np.cos(2 * np.pi * fc * t)
    return baseband_signal, carrier_signal, modulated_signal

# Time vector
t = np.linspace(0, 1, 1000)

# Initial parameters
Ac_init = 1.0
fc_init = 10.0
Am_init = 1.0
fm_init = 100.0

# Generate initial signals
baseband_signal, carrier_signal, modulated_signal = generate_am_signal(Ac_init, fc_init, Am_init, fm_init, t)

# Create the figure and axes
fig, axs = plt.subplots(3, 1, figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.3)

# Plot baseband signal
line_baseband, = axs[0].plot(t, baseband_signal, label="Baseband Signal (M(t))")
axs[0].set_title("Baseband Signal (M(t))")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Amplitude")
axs[0].grid()

# Plot carrier signal
line_carrier, = axs[1].plot(t, carrier_signal, label="Carrier Signal (C(t))", color='orange')
axs[1].set_title("Carrier Signal (C(t))")
axs[1].set_xlabel("Time (μs)")
axs[1].set_ylabel("Amplitude")
axs[1].grid()

# Plot modulated signal
line_modulated, = axs[2].plot(t, modulated_signal, label="AM Modulated Signal (S(t))", color='green')
axs[2].set_title("AM Modulated Signal (S(t))")
axs[2].set_xlabel("Time (μs)")
axs[2].set_ylabel("Amplitude")
axs[2].grid()

# Add sliders for parameters
axcolor = 'lightgoldenrodyellow'
ax_Ac = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_fc = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_Am = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_fm = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)

slider_Ac = Slider(ax_Ac, 'Ac', 0.1, 5.0, valinit=Ac_init)
slider_fc = Slider(ax_fc, 'fc', 1.0, 50.0, valinit=fc_init)
slider_Am = Slider(ax_Am, 'Am', 0.1, 5.0, valinit=Am_init)
slider_fm = Slider(ax_fm, 'fm', 1.0, 500.0, valinit=fm_init)

# Update function with auto-rescaling of y-axis
def update(val):
    Ac = slider_Ac.val
    fc = slider_fc.val
    Am = slider_Am.val
    fm = slider_fm.val
    baseband_signal, carrier_signal, modulated_signal = generate_am_signal(Ac, fc, Am, fm, t)
    line_baseband.set_ydata(baseband_signal)
    line_carrier.set_ydata(carrier_signal)
    line_modulated.set_ydata(modulated_signal)
    axs[0].set_ylim(baseband_signal.min() - 0.5, baseband_signal.max() + 0.5)
    axs[1].set_ylim(carrier_signal.min() - 0.5, carrier_signal.max() + 0.5)
    axs[2].set_ylim(modulated_signal.min() - 0.5, modulated_signal.max() + 0.5)
    fig.canvas.draw_idle()

# Connect sliders to update function
slider_Ac.on_changed(update)
slider_fc.on_changed(update)
slider_Am.on_changed(update)
slider_fm.on_changed(update)

plt.show()
