import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def generate_qam_constellation(N):
    """
    Generates a QAM constellation for N symbols.

    Parameters:
        N (int): Number of symbols (e.g., 16 for 16-QAM, 64 for 64-QAM).

    Returns:
        constellation (ndarray): Array of complex numbers representing the QAM constellation points.
    """
    if not (np.log2(N) % 1 == 0):
        raise ValueError("N must be a power of 2 (e.g., 4, 16, 64, ...).")

    M = int(np.sqrt(N))  # Dimensions of the QAM grid (M x M)
    if M * M != N:
        raise ValueError("N must have an integer square root (e.g., 4, 16, 64, ...).")

    # Generate evenly spaced grid points
    x = np.arange(-M + 1, M, 2)
    y = np.arange(-M + 1, M, 2)
    xv, yv = np.meshgrid(x, y)

    # Combine into complex symbols
    constellation = xv.flatten() + 1j * yv.flatten()

    # Normalize average power to 1
    constellation /= np.sqrt(np.mean(np.abs(constellation) ** 2))

    return constellation

def plot_qam_constellation(ax, constellation, noise_std):
    """
    Plots the QAM constellation with optional Gaussian noise.

    Parameters:
        ax (Axes): Matplotlib axes object.
        constellation (ndarray): Array of complex numbers representing the QAM constellation points.
        noise_std (float): Standard deviation of the Gaussian noise to be added.
    """
    ax.clear()

    if noise_std > 0:
        noise = noise_std * (np.random.randn(len(constellation)) + 1j * np.random.randn(len(constellation)))
        noisy_constellation = constellation + noise
    else:
        noisy_constellation = constellation

    ax.scatter(noisy_constellation.real, noisy_constellation.imag, c='blue', label='Constellation Points')
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title(f'QAM Constellation (N = {len(constellation)})')
    ax.set_xlabel('In-Phase')
    ax.set_ylabel('Quadrature')
    ax.legend()
    ax.axis('equal')

def update(val):
    """Update the plot based on slider values."""
    try:
        N = int(2 ** int(slider_symbols.val))  # Convert slider value to power of 2
        noise_std = slider_noise.val  # Directly use slider value for noise standard deviation
        constellation = generate_qam_constellation(N)
        plot_qam_constellation(ax, constellation, noise_std)
        fig.canvas.draw_idle()
    except ValueError as e:
        ax.clear()
        ax.text(0.5, 0.5, str(e), transform=ax.transAxes, ha='center', va='center', fontsize=12, color='red')
        fig.canvas.draw_idle()

def reset(event):
    """Reset sliders to their initial positions."""
    slider_symbols.reset()
    slider_noise.reset()

# Initialize the figure and axes
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.25)

# Initial parameters
initial_symbols = 16
initial_noise_std = 0.1

# Generate initial QAM constellation
constellation = generate_qam_constellation(initial_symbols)
plot_qam_constellation(ax, constellation, initial_noise_std)

# Add sliders
ax_symbols = plt.axes([0.2, 0.1, 0.65, 0.03])
ax_noise = plt.axes([0.2, 0.05, 0.65, 0.03])

slider_symbols = Slider(ax_symbols, 'Log2(Sym)', 2, 6, valinit=np.log2(initial_symbols), valstep=1)
slider_noise = Slider(ax_noise, 'Noise (Std)', 0.01, 1.0, valinit=initial_noise_std)

slider_symbols.on_changed(update)
slider_noise.on_changed(update)

# Add reset button
reset_ax = plt.axes([0.8, 0.01, 0.1, 0.04])
button = Button(reset_ax, 'Reset')
button.on_clicked(reset)

plt.show()
