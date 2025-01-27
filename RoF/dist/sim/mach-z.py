import numpy as np
import matplotlib.pyplot as plt

def mach_zehnder_modulator(amplitude, phase, phase_shift_1=0, phase_shift_2=0):
    """
    Simulate a Mach-Zehnder Modulator.

    Parameters:
        amplitude (ndarray): Input amplitude of the optical signal.
        phase (ndarray): Input phase of the optical signal (in radians).
        phase_shift_1 (float): Phase shift in the first arm of the MZM (in radians).
        phase_shift_2 (float): Phase shift in the second arm of the MZM (in radians).

    Returns:
        output_amplitude (ndarray): Output amplitude of the optical signal.
        output_phase (ndarray): Output phase of the optical signal (in radians).
    """
    # Split the input signal into two arms
    arm_1 = amplitude * np.exp(1j * (phase + phase_shift_1))
    arm_2 = amplitude * np.exp(1j * (phase + phase_shift_2))

    # Combine the two arms (interference)
    output_signal = arm_1 + arm_2

    # Extract amplitude and phase of the output signal
    output_amplitude = np.abs(output_signal)
    output_phase = np.angle(output_signal)

    return output_amplitude, output_phase

def plot_signals(input_amplitude, input_phase, output_amplitude, output_phase):
    """
    Plot input and output signals (amplitude and phase).

    Parameters:
        input_amplitude (ndarray): Input amplitude of the optical signal.
        input_phase (ndarray): Input phase of the optical signal (in radians).
        output_amplitude (ndarray): Output amplitude of the optical signal.
        output_phase (ndarray): Output phase of the optical signal (in radians).
    """
    time = np.arange(len(input_amplitude))

    plt.figure(figsize=(12, 8))

    # Input amplitude
    plt.subplot(2, 2, 1)
    plt.plot(time, input_amplitude, label='Input Amplitude')
    plt.title("Input Amplitude")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()

    # Input phase
    plt.subplot(2, 2, 2)
    plt.plot(time, input_phase, label='Input Phase', color='orange')
    plt.title("Input Phase")
    plt.xlabel("Time")
    plt.ylabel("Phase (radians)")
    plt.grid(True)
    plt.legend()

    # Output amplitude
    plt.subplot(2, 2, 3)
    plt.plot(time, output_amplitude, label='Output Amplitude', color='green')
    plt.title("Output Amplitude")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()

    # Output phase
    plt.subplot(2, 2, 4)
    plt.plot(time, output_phase, label='Output Phase', color='red')
    plt.title("Output Phase")
    plt.xlabel("Time")
    plt.ylabel("Phase (radians)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

# Example usage
try:
    # Generate input signal (sinusoidal optical signal)
    time_steps = 100
    t = np.linspace(0, 1, time_steps)
    input_amplitude = 1 + 0.5 * np.sin(2 * np.pi * 10 * t)  # Sinusoidal amplitude
    input_phase = 2 * np.pi * t  # Linear phase progression

    # Modulate using Mach-Zehnder Modulator
    phase_shift_1 = float(input("Enter phase shift for arm 1 (in radians): "))
    phase_shift_2 = float(input("Enter phase shift for arm 2 (in radians): "))

    output_amplitude, output_phase = mach_zehnder_modulator(input_amplitude, input_phase, phase_shift_1, phase_shift_2)

    # Plot the results
    plot_signals(input_amplitude, input_phase, output_amplitude, output_phase)
except Exception as e:
    print(f"Error: {e}")
