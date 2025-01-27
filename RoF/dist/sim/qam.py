import numpy as np
import matplotlib.pyplot as plt

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

def plot_qam_constellation(constellation, noise_std=0):
    """
    Plots the QAM constellation with optional Gaussian noise.

    Parameters:
        constellation (ndarray): Array of complex numbers representing the QAM constellation points.
        noise_std (float): Standard deviation of the Gaussian noise to be added.
    """
    if noise_std > 0:
        noise = noise_std * (np.random.randn(len(constellation)) + 1j * np.random.randn(len(constellation)))
        noisy_constellation = constellation + noise
    else:
        noisy_constellation = constellation

    plt.figure(figsize=(8, 8))
    plt.scatter(noisy_constellation.real, noisy_constellation.imag, c='blue', label='Constellation Points')
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(f'QAM Constellation (N = {len(constellation)})')
    plt.xlabel('In-Phase')
    plt.ylabel('Quadrature')
    plt.legend()
    plt.axis('equal')
    plt.show()

# Example usage:
try:
    N = int(input("Enter the number of symbols (e.g., 16, 64): "))
    noise_std = float(input("Enter the noise standard deviation (0 for no noise): "))
    
    constellation = generate_qam_constellation(N)
    plot_qam_constellation(constellation, noise_std)
except ValueError as e:
    print(f"Error: {e}")
