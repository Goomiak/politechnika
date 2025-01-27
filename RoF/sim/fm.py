import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Function to generate FM modulated signal
def generate_fm_signal(Ac, fc, Am, fm, kf, t):
    beta = (kf * Am) / fm  # Modulation index
    modulated_signal = Ac * np.cos(2 * np.pi * fc * t + beta * np.sin(2 * np.pi * fm * t))
    return modulated_signal, beta

# Time vector
t = np.linspace(0, 1, 1000)

# Initial parameters
Ac_init = 1.0  # Carrier amplitude
fc_init = 10.0  # Carrier frequency
Am_init = 1.0  # Modulating signal amplitude
fm_init = 1.0  # Modulating signal frequency
kf_init = 50.0  # Frequency sensitivity (Hz/V)

# Generate initial signals
modulated_signal, beta_init = generate_fm_signal(Ac_init, fc_init, Am_init, fm_init, kf_init, t)

# Create the figure and axes
fig, axs = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [1, 2]})
plt.subplots_adjust(left=0.1, bottom=0.3, hspace=0.5)

# Plot modulation index (β)
axs[0].text(0.1, 0.5, f'Modulation Index (β): {beta_init:.2f}', fontsize=12)
axs[0].axis("off")

# Modulated signal plot
line_modulated, = axs[1].plot(t, modulated_signal, label="FM Modulated Signal (S(t))", color='green')
axs[1].set_title("FM Modulated Signal (S(t))")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Amplitude")
axs[1].grid()

# Add sliders for parameters
axcolor = 'lightgoldenrodyellow'
ax_Ac = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_fc = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_Am = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_fm = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)

slider_Ac = Slider(ax_Ac, 'Ac', 0.1, 5.0, valinit=Ac_init)
slider_fc = Slider(ax_fc, 'fc', 1.0, 50.0, valinit=fc_init)
slider_Am = Slider(ax_Am, 'Am', 0.1, 5.0, valinit=Am_init)
slider_fm = Slider(ax_fm, 'fm', 0.1, 10.0, valinit=fm_init)

# Update function
def update(val):
    Ac = slider_Ac.val
    fc = slider_fc.val
    Am = slider_Am.val
    fm = slider_fm.val
    modulated_signal, beta = generate_fm_signal(Ac, fc, Am, fm, kf_init, t)
    axs[0].clear()
    axs[0].text(0.1, 0.5, f'Modulation Index (β): {beta:.2f}', fontsize=12)
    axs[0].axis("off")
    line_modulated.set_ydata(modulated_signal)
    axs[1].set_ylim(modulated_signal.min() - 0.5, modulated_signal.max() + 0.5)
    fig.canvas.draw_idle()

# Connect sliders to update function
slider_Ac.on_changed(update)
slider_fc.on_changed(update)
slider_Am.on_changed(update)
slider_fm.on_changed(update)

plt.show()