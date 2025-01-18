import numpy as np
import matplotlib.pyplot as plt

def rf_modulation():
    f_rf = 5e3
    f_light = 2e5
    A_rf = 1.0
    A_light = 2.0
    t = np.linspace(0, 0.01, 1000)
    rf_signal = A_rf * np.cos(2 * np.pi * f_rf * t)
    modulated_signal = (A_light + rf_signal) * np.cos(2 * np.pi * f_light * t)
    
    plt.figure(figsize=(10, 8))
    plt.subplot(3, 1, 1)
    plt.plot(t, rf_signal)
    plt.title("Sygnał RF (5 kHz)")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")
    
    plt.subplot(3, 1, 2)
    plt.plot(t, modulated_signal)
    plt.title("Sygnał światła z modulacją amplitudy")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")
    
    plt.subplot(3, 1, 3)
    plt.plot(t[0:200], modulated_signal[0:200])
    plt.title("Przybliżenie - modulacja amplitudy sygnałem RF")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")
    
    plt.tight_layout()
    plt.show()

def optical_attenuation():
    wavelength = 1550e-9
    initial_intensity = 1.0
    attenuation_coefficient = 0.2
    distances = np.linspace(0, 100, 500)
    intensity = initial_intensity * np.exp(-attenuation_coefficient * distances)
    
    plt.figure(figsize=(10, 5))
    plt.plot(distances, intensity)
    plt.title("Tłumienie sygnału optycznego w światłowodzie")
    plt.xlabel("Odległość [km]")
    plt.ylabel("Natężenie sygnału")
    plt.grid()
    plt.show()

def single_slit_diffraction():
    wavelength = 500e-9
    slit_width = 1e-6
    screen_distance = 1
    x = np.linspace(-0.01, 0.01, 1000)
    beta = (np.pi * slit_width * x) / (wavelength * screen_distance)
    intensity = (np.sin(beta) / beta) ** 2
    intensity[beta == 0] = 1.0
    
    plt.figure(figsize=(10, 5))
    plt.plot(x * 1e3, intensity)
    plt.title("Dyfrakcja pojedynczej szczeliny")
    plt.xlabel("Pozycja na ekranie [mm]")
    plt.ylabel("Natężenie")
    plt.grid()
    plt.show()

def diffraction_grating():
    wavelength = 500e-9
    grating_spacing = 2e-6
    num_slits = 5
    screen_distance = 1
    x = np.linspace(-0.01, 0.01, 1000)
    beta = (np.pi * grating_spacing * x) / (wavelength * screen_distance)
    single_slit = (np.sin(beta) / beta) ** 2
    single_slit[beta == 0] = 1.0
    delta = (2 * np.pi * grating_spacing * x) / (wavelength * screen_distance)
    multi_slit = (np.sin(num_slits * delta / 2) / np.sin(delta / 2)) ** 2
    intensity = single_slit * multi_slit
    
    plt.figure(figsize=(10, 5))
    plt.plot(x * 1e3, intensity)
    plt.title("Dyfrakcja przez siatkę dyfrakcyjną")
    plt.xlabel("Pozycja na ekranie [mm]")
    plt.ylabel("Natężenie")
    plt.grid()
    plt.show()

def sim_interferencja_younga():
    wavelength = 500e-9  # Długość fali światła (500 nm)
    d = 2e-6  # Odległość między szczelinami (2 mikrometry)
    screen_distance = 1  # Odległość od szczelin do ekranu (1 m)
    x = np.linspace(-0.01, 0.01, 1000)  # Pozycje na ekranie (w metrach)
    delta = (2 * np.pi * d * x) / (wavelength * screen_distance)
    intensity = (np.cos(delta / 2)) ** 2

    plt.figure(figsize=(10, 5))
    plt.plot(x * 1e3, intensity, label="Interferencja dwóch szczelin")
    plt.title("Interferencja światła (eksperyment Younga)")
    plt.xlabel("Pozycja na ekranie [mm]")
    plt.ylabel("Natężenie")
    plt.grid()
    plt.legend()
    plt.show()

def sim_interferencja_fal_kulistych():
    wavelength = 500e-9  # Długość fali światła (500 nm)
    source_separation = 5e-3  # Odległość między źródłami (5 mm)
    grid_size = 200  # Rozdzielczość siatki symulacji
    extent = 1e-2  # Obszar symulacji (10 mm x 10 mm)

    x = np.linspace(-extent, extent, grid_size)
    y = np.linspace(-extent, extent, grid_size)
    X, Y = np.meshgrid(x, y)
    source1 = np.array([-source_separation / 2, 0])
    source2 = np.array([source_separation / 2, 0])
    r1 = np.sqrt((X - source1[0])**2 + (Y - source1[1])**2)
    r2 = np.sqrt((X - source2[0])**2 + (Y - source2[1])**2)
    wave1 = np.cos(2 * np.pi * r1 / wavelength)
    wave2 = np.cos(2 * np.pi * r2 / wavelength)
    intensity = (wave1 + wave2)**2

    plt.figure(figsize=(8, 8))
    plt.imshow(intensity, extent=(-extent * 1e3, extent * 1e3, -extent * 1e3, extent * 1e3), cmap='inferno')
    plt.title("Interferencja fal kulistych")
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.colorbar(label="Intensywność")
    plt.show()

def sim_modulacja_am():
    fs = 1e6  # Częstotliwość próbkowania (1 MHz)
    t = np.linspace(0, 1e-3, int(fs * 1e-3))
    carrier_freq = 100e3  # Częstotliwość fali nośnej (100 kHz)
    signal_freq = 1e3  # Częstotliwość sygnału (1 kHz)

    signal = np.sin(2 * np.pi * signal_freq * t)
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    modulated_signal = (1 + signal) * carrier

    plt.figure(figsize=(12, 6))
    plt.subplot(3, 1, 1)
    plt.plot(t * 1e3, signal, label="Sygnał modulujący")
    plt.title("Sygnał modulujący (1 kHz)")
    plt.xlabel("Czas [ms]")
    plt.ylabel("Amplituda")
    plt.grid()
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(t * 1e3, carrier, label="Fala nośna (100 kHz)")
    plt.title("Fala nośna")
    plt.xlabel("Czas [ms]")
    plt.ylabel("Amplituda")
    plt.grid()
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(t * 1e3, modulated_signal, label="Sygnał zmodulowany")
    plt.title("Modulacja amplitudy (AM)")
    plt.xlabel("Czas [ms]")
    plt.ylabel("Amplituda")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()

def sim_modulacja_pm():
    fs = 1e6  # Częstotliwość próbkowania (1 MHz)
    t = np.linspace(0, 1e-3, int(fs * 1e-3))
    carrier_freq = 100e3  # Częstotliwość fali nośnej (100 kHz)
    signal_freq = 1e3  # Częstotliwość sygnału (1 kHz)

    signal = np.sin(2 * np.pi * signal_freq * t)
    modulated_phase = np.sin(2 * np.pi * carrier_freq * t + np.pi * signal)

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t * 1e3, signal, label="Sygnał modulujący")
    plt.title("Sygnał modulujący (1 kHz)")
    plt.xlabel("Czas [ms]")
    plt.ylabel("Amplituda")
    plt.grid()
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(t * 1e3, modulated_phase, label="Sygnał zmodulowany fazowo")
    plt.title("Modulacja fazy (PM)")
    plt.xlabel("Czas [ms]")
    plt.ylabel("Amplituda")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()

def sim_modulacja_fm():
    fs = 1e6  # Częstotliwość próbkowania (1 MHz)
    t = np.linspace(0, 1e-3, int(fs * 1e-3))
    carrier_freq = 100e3  # Częstotliwość fali nośnej (100 kHz)
    signal_freq = 1e3  # Częstotliwość sygnału (1 kHz)
    freq_deviation = 50e3  # Maksymalne odchylenie częstotliwości (50 kHz)

    signal = np.sin(2 * np.pi * signal_freq * t)
    instantaneous_freq = carrier_freq + freq_deviation * signal
    modulated_freq = np.sin(2 * np.pi * np.cumsum(instantaneous_freq) / fs)

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t * 1e3, signal, label="Sygnał modulujący")
    plt.title("Sygnał modulujący (1 kHz)")
    plt.xlabel("Czas [ms]")
    plt.ylabel("Amplituda")
    plt.grid()
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(t * 1e3, modulated_freq, label="Sygnał zmodulowany częstotliwościowo")
    plt.title("Modulacja częstotliwości (FM)")
    plt.xlabel("Czas [ms]")
    plt.ylabel("Amplituda")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()

def sim_modulacja_polaryzacji():
    fs = 1e6  # Częstotliwość próbkowania (1 MHz)
    t = np.linspace(0, 1e-3, int(fs * 1e-3))
    signal_freq = 1e3  # Częstotliwość sygnału (1 kHz)
    signal = np.sin(2 * np.pi * signal_freq * t)

    theta = np.pi / 4  # Kąt polaryzacji (45 stopni)
    modulated_signal_x = (1 + signal) * np.cos(theta)
    modulated_signal_y = (1 + signal) * np.sin(theta)

    plt.figure(figsize=(10, 6))
    plt.quiver(np.zeros(len(t)), np.zeros(len(t)), modulated_signal_x, modulated_signal_y, angles='xy', scale_units='xy', scale=0.01, color="blue")
    plt.title("Modulacja polaryzacji światła")
    plt.xlabel("Komponent X")
    plt.ylabel("Komponent Y")
    plt.grid()
    plt.show()

def sim_modulacja_qam():
    fs = 1e6  # Częstotliwość próbkowania (1 MHz)
    t = np.linspace(0, 1e-3, int(fs * 1e-3))
    carrier_freq = 100e3  # Częstotliwość fali nośnej (100 kHz)
    signal_freq = 1e3  # Częstotliwość sygnału (1 kHz)

    signal_i = np.sin(2 * np.pi * signal_freq * t)
    signal_q = np.cos(2 * np.pi * signal_freq * t)
    qam_signal = signal_i * np.cos(2 * np.pi * carrier_freq * t) + signal_q * np.sin(2 * np.pi * carrier_freq * t)

    plt.figure(figsize=(12, 6))
    plt.plot(t * 1e3, qam_signal, label="Sygnał zmodulowany (QAM)")
    plt.title("Modulacja kwadraturowa (QAM)")
    plt.xlabel("Czas [ms]")
    plt.ylabel("Amplituda")
    plt.grid()
    plt.legend()
    plt.show()

def sim_modulator_mach_zehnder():
    f_signal = 1e3  # Częstotliwość sygnału elektrycznego (1 kHz)
    f_light = 1e5  # Częstotliwość światła (fala nośna - 100 kHz)
    V_pi = 5  # Napięcie powodujące zmianę fazy o π
    V_signal = 3  # Amplituda napięcia sygnału elektrycznego
    A_light = 1.0  # Amplituda fali nośnej
    t = np.linspace(0, 0.01, 1000)  # Czas od 0 do 10 ms

    V = V_signal * np.sin(2 * np.pi * f_signal * t)
    phase_shift = (np.pi / V_pi) * V
    modulated_signal = A_light * np.cos(2 * np.pi * f_light * t + phase_shift)

    plt.figure(figsize=(10, 8))
    plt.subplot(3, 1, 1)
    plt.plot(t, V)
    plt.title("Sygnał elektryczny (1 kHz)")
    plt.xlabel("Czas [s]")
    plt.ylabel("Napięcie [V]")

    plt.subplot(3, 1, 2)
    plt.plot(t, phase_shift)
    plt.title("Zmiana fazy sygnału optycznego")
    plt.xlabel("Czas [s]")
    plt.ylabel("Faza [rad]")

    plt.subplot(3, 1, 3)
    plt.plot(t, modulated_signal)
    plt.title("Sygnał światła modulowanego (Mach-Zehnder)")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")

    plt.tight_layout()
    plt.show()

def sim_charakterystyka_spektralna_detektora():
    wavelengths = np.linspace(400, 1600, 500)
    responsivity_peak = 0.8
    peak_wavelength = 950
    bandwidth = 300
    responsivity = responsivity_peak * np.exp(-((wavelengths - peak_wavelength) ** 2) / (2 * bandwidth ** 2))
    
    plt.figure(figsize=(10, 5))
    plt.plot(wavelengths, responsivity, label="Responsywność detektora")
    plt.title("Charakterystyka spektralna detektora fotonicznego")
    plt.xlabel("Długość fali [nm]")
    plt.ylabel("Responsywność [A/W]")
    plt.legend()
    plt.grid()
    plt.show()

def sim_generacja_sygnalu_mikrofalowego():
    f_laser1 = 2e14
    f_laser2 = 2e14 + 1e9
    A_laser = 1.0
    time = np.linspace(0, 1e-6, 1000)
    
    laser1 = A_laser * np.cos(2 * np.pi * f_laser1 * time)
    laser2 = A_laser * np.cos(2 * np.pi * f_laser2 * time)
    microwave_signal = 2 * A_laser * np.cos(2 * np.pi * (f_laser2 - f_laser1) * time)
    
    plt.figure(figsize=(10, 8))
    plt.subplot(3, 1, 1)
    plt.plot(time, laser1, label="Laser 1 (200 THz)")
    plt.title("Sygnał lasera 1")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")
    
    plt.subplot(3, 1, 2)
    plt.plot(time, laser2, label="Laser 2 (200 THz + 1 GHz różnicy)", color="orange")
    plt.title("Sygnał lasera 2")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")
    
    plt.subplot(3, 1, 3)
    plt.plot(time, microwave_signal, label="Sygnał RF (1 GHz)", color="green")
    plt.title("Generacja sygnału mikrofalowego (1 GHz)")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")
    
    plt.tight_layout()
    plt.show()

def sim_wzmacniacz_edfa():
    distance = np.linspace(0, 20, 500)
    input_power = 1e-3
    gain = 3
    loss = 0.2
    output_power = input_power * 10 ** ((gain - loss) * distance / 10)
    
    plt.figure(figsize=(10, 5))
    plt.plot(distance, output_power, label="Moc wyjściowa")
    plt.title("Wzmocnienie sygnału optycznego (EDFA)")
    plt.xlabel("Odległość [km]")
    plt.ylabel("Moc [W]")
    plt.legend()
    plt.grid()
    plt.show()


def show_menu():
    print("Wybierz symulację:")
    print("1. Transmisja sygnału RF za pomocą modulacji światła")
    print("2. Transmisja sygnałów w światłowodzie (z tłumieniem)")
    print("3. Dyfrakcja pojedynczej szczeliny")
    print("4. Dyfrakcja przez siatkę dyfrakcyjną")
    print("5. Interferencja dwóch szczelin")
    print("6. Interferencja dwóch fal kulistych")
    print("7. Modulacja AM")
    print("8. Modulacja PM")
    print("9. Modulacja FM")
    print("10. Modulacja polaryzacji światła")
    print("11. Modulacja QAM")
    print("12. Modulator Mach-Zehndera")
    print("13. Charakterystyka spektralna detektora")
    print("14. Generacja sygnału mikrofalowego")
    print("15. Wzmacniacz EDFA")
    print("0. Wyjdź")

def main():
    while True:
        show_menu()
        choice = input("Twój wybór: ")
        if choice == "1":
            rf_modulation()
        elif choice == "2":
            optical_attenuation()
        elif choice == "3":
            single_slit_diffraction()
        elif choice == "4":
            diffraction_grating()
        elif choice == "5":
            sim_interferencja_younga()
        elif choice == "6":
            sim_interferencja_fal_kulistych()
        elif choice == "7":
            sim_modulacja_am()
        elif choice == "8":
            sim_modulacja_pm()
        elif choice == "9":
            sim_modulacja_fm()
        elif choice == "10":
            sim_modulacja_polaryzacji()
        elif choice == "11":
            sim_modulacja_qam()
        elif choice == "12":
            sim_modulator_mach_zehnder()
        elif choice == "13":
            sim_charakterystyka_spektralna_detektora()
        elif choice == "14":
            sim_generacja_sygnalu_mikrofalowego()
        elif choice == "15":
            sim_wzmacniacz_edfa()
        elif choice == "0":
            print("Do widzenia!")
            break
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")

if __name__ == "__main__":
    main()
