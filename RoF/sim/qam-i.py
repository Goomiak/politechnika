import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

def generate_qam_constellation(N, iterations, noise_std):
    """
    Generates a QAM constellation for N symbols with multiple iterations and noise.

    Parameters:
        N (int): Number of symbols (e.g., 16 for 16-QAM, 64 for 64-QAM).
        iterations (int): Number of repetitions for each symbol to generate additional points.
        noise_std (float): Standard deviation of the Gaussian noise to be added.

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
    base_constellation = xv.flatten() + 1j * yv.flatten()

    # Normalize average power to 1
    base_constellation /= np.sqrt(np.mean(np.abs(base_constellation) ** 2))

    # Repeat the constellation for iterations and add random jitter
    jitter = noise_std * (np.random.randn(len(base_constellation) * iterations) + 1j * np.random.randn(len(base_constellation) * iterations))
    constellation = np.tile(base_constellation, iterations) + jitter

    return constellation

def plot_qam_constellation(ax, constellation):
    """
    Plots the QAM constellation.

    Parameters:
        ax (Axes): Matplotlib axes object.
        constellation (ndarray): Array of complex numbers representing the QAM constellation points.
    """
    ax.clear()
    ax.scatter(constellation.real, constellation.imag, c='blue', label='Constellation Points', alpha=0.6)
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title(f'QAM Constellation (N = {len(set(constellation))}, Iterations = {iterations})')
    ax.set_xlabel('In-Phase')
    ax.set_ylabel('Quadrature')
    ax.legend()
    ax.axis('equal')

def update(val):
    """Update the plot based on slider and button values."""
    global iterations, noise_std
    try:
        N = int(selected_symbols.value_selected)  # Get selected number of symbols
        iterations = int(slider_iterations.val)  # Get slider value for iterations
        noise_std = slider_noise.val  # Get slider value for noise
        constellation = generate_qam_constellation(N, iterations, noise_std)
        plot_qam_constellation(ax, constellation)
        fig.canvas.draw_idle()
    except ValueError as e:
        ax.clear()
        ax.text(0.5, 0.5, str(e), transform=ax.transAxes, ha='center', va='center', fontsize=12, color='red')
        fig.canvas.draw_idle()

def reset(event):
    """Reset sliders and buttons to their initial positions."""
    slider_iterations.reset()
    slider_noise.reset()
    selected_symbols.set_active(1)  # Reset to 16 symbols

# Initialize the figure and axes
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.3, bottom=0.3)

# Initial parameters
initial_symbols = 16
iterations = 10
noise_std = 0.1

# Generate initial QAM constellation
constellation = generate_qam_constellation(initial_symbols, iterations, noise_std)
plot_qam_constellation(ax, constellation)

# Add slider for iterations
ax_iterations = plt.axes([0.2, 0.15, 0.65, 0.03])
slider_iterations = Slider(ax_iterations, 'Iterations', 1, 100, valinit=iterations, valstep=1)
slider_iterations.on_changed(update)

# Add slider for noise standard deviation
ax_noise = plt.axes([0.2, 0.1, 0.65, 0.03])
slider_noise = Slider(ax_noise, 'Noise (Std)', 0.01, 1.0, valinit=noise_std)
slider_noise.on_changed(update)

# Add radio buttons for symbol selection
symbols = ['4', '16', '64', '256', '1024']
ax_symbols = plt.axes([0.01, 0.3, 0.2, 0.5])
selected_symbols = RadioButtons(ax_symbols, symbols, active=symbols.index(str(initial_symbols)))
selected_symbols.on_clicked(update)

# Add reset button
reset_ax = plt.axes([0.8, 0.01, 0.1, 0.04])
button = Button(reset_ax, 'Reset')
button.on_clicked(reset)

plt.show()
