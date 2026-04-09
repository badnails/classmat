import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# Abstract Base Class for Continuous-Time Signals
# =====================================================
class ContinuousSignal:
    """
    Abstract base class for all continuous-time signals.
    Every signal must be defined over a time axis t.
    """

    def __init__(self, t):
        self.t = t

    def values(self):
        """
        Returns the signal values evaluated over time axis t.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def plot(self, title="Signal"):
        """
        Plot the signal in the time domain.
        """
        plt.plot(self.t, self.values())
        plt.xlabel("Time (t)")
        plt.ylabel("Amplitude")
        plt.title(title)
        plt.grid(True)
        plt.show()


# =====================================================
# Signal Generator Class
# =====================================================
class SignalGenerator(ContinuousSignal):
    """
    Generates various continuous-time signals.
    Each method returns a numpy array of signal samples.
    """

    def sine(self, amplitude, frequency):
        """Generate a sine wave."""
        return amplitude * np.sin(2 * np.pi * frequency * self.t)

    def cosine(self, amplitude, frequency):
        """Generate a cosine wave."""
        return amplitude * np.cos(2 * np.pi * frequency * self.t)

    def square(self, amplitude, frequency):
        """Generate a square wave using sign of sine."""
        return amplitude * np.sign(np.sin(2 * np.pi * frequency * self.t))

    def sawtooth(self, amplitude, frequency):
        """Generate a sawtooth wave."""
        return amplitude * 2 * (frequency * self.t - np.floor(0.5 + frequency * self.t))

    def triangle(self, amplitude, frequency):
        """Generate a triangle wave."""
        return (2 * amplitude / np.pi) * np.arcsin(np.sin(2 * np.pi * frequency * self.t))

    def cubic(self, coefficient):
        """Generate a cubic polynomial signal."""
        return coefficient * (self.t ** 3)

    def parabolic(self, coefficient):
        """Generate a parabolic signal."""
        return coefficient * (self.t ** 2)

    def rectangular(self, width):
        """Generate a rectangular window centered at t=0."""
        return np.where(np.abs(self.t) <= width / 2, 1.0, 0.0)

    def pulse(self, start, end):
        """Generate a finite pulse active between start and end."""
        return np.where((self.t >= start) & (self.t <= end), 1.0, 0.0)


# =====================================================
# Composite Signal Class
# =====================================================
class CompositeSignal(ContinuousSignal):
    """
    Combines multiple signals into a single composite signal.
    """

    def __init__(self, t):
        super().__init__(t)
        self.components = []

    def add_component(self, signal):
        """
        Add a signal component to the composite signal.
        """
        self.components.append(signal)

    def values(self):
        """
        Sum all signal components.
        """
        values = np.zeros_like(self.t)
        for component in self.components:
            values += component
        return values


# =====================================================
# Continuous Fourier Transform Analyzer
# =====================================================
class CFTAnalyzer:
    """
    Computes the Continuous Fourier Transform (CFT)
    using numerical integration (np.trapz).
    """

    def __init__(self, signal, t, frequencies):
        self.signal = signal
        self.t = t
        self.frequencies = frequencies

    def compute_cft(self):
        """
        Compute real and imaginary parts of the CFT.
        """
        f_t = self.signal.values()
        F_a = np.zeros_like(self.frequencies)
        F_b = np.zeros_like(self.frequencies)
        
        for i, f in enumerate(self.frequencies):
            F_a[i] = np.trapezoid(f_t * np.cos(2 * np.pi * f * self.t), self.t)
            F_b[i] = -np.trapezoid(f_t * np.sin(2 * np.pi * f * self.t), self.t)
        
        return (F_a, F_b)

    def plot_spectrum(self):
        """
        Plot magnitude spectrum of the signal.
        """
        F_a, F_b = self.compute_cft()
        mag = np.sqrt(F_a**2 + F_b**2)
        
        plt.figure(figsize=(10, 4))
        plt.plot(self.frequencies, mag)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.title("Magnitude Spectrum")
        plt.grid(True)
        plt.show()

    def plot_phase(self):
        """
        Plot phase spectrum of the signal.
        """
        F_a, F_b = self.compute_cft()
        phase = np.arctan2(F_b, F_a)
        
        plt.figure(figsize=(10, 4))
        plt.plot(self.frequencies, phase)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Phase (radians)")
        plt.title("Phase Spectrum")
        plt.grid(True)
        plt.show()


# =====================================================
# Inverse Continuous Fourier Transform
# =====================================================
class InverseCFT:
    """
    Reconstructs time-domain signal using ICFT.
    """

    def __init__(self, spectrum, frequencies, t):
        self.spectrum = spectrum
        self.frequencies = frequencies
        self.t = t

    def reconstruct(self):
        """
        Perform inverse CFT using numerical integration.
        """
        F_a, F_b = self.spectrum
        f_t = np.zeros_like(self.t)
        
        for i, tv in enumerate(self.t):
            f_t[i] = np.trapezoid(F_a * np.cos(2 * np.pi * self.frequencies * tv) - F_b * np.sin(2 * np.pi * self.frequencies * tv), self.frequencies)
        
        return f_t


# =====================================================
# Complex Signal CFT Analyzer (for modulated signals)
# =====================================================
class ComplexCFTAnalyzer:
    """
    Computes CFT for complex-valued signals.
    """
    def __init__(self, signal_real, signal_imag, t, frequencies):
        self.signal_real = signal_real
        self.signal_imag = signal_imag
        self.t = t
        self.frequencies = frequencies
    
    def compute_cft(self):
        """
        Compute CFT of complex signal: y(t) = y_real(t) + j*y_imag(t)
        Y(f) = ∫ y(t) * e^(-j2πft) dt
        """
        y_real = self.signal_real
        y_imag = self.signal_imag
        F_a = np.zeros_like(self.frequencies)
        F_b = np.zeros_like(self.frequencies)
        
        for i, f in enumerate(self.frequencies):
            cos_term = np.cos(2 * np.pi * f * self.t)
            sin_term = np.sin(2 * np.pi * f * self.t)
            # Real part: ∫ (y_real*cos + y_imag*sin) dt
            F_a[i] = np.trapezoid(y_real * cos_term + y_imag * sin_term, self.t)
            # Imag part: ∫ (-y_real*sin + y_imag*cos) dt = -∫ (y_real*sin - y_imag*cos) dt
            F_b[i] = -np.trapezoid(y_real * sin_term - y_imag * cos_term, self.t)
        
        return (F_a, F_b)


# =====================================================
# Main Execution - Phase Shift and Time Compression
# =====================================================
if __name__ == "__main__":
    # Define time axis: t ∈ [-5, 5] with at least 2000 samples
    t = np.linspace(-5, 5, 2000)
    
    # Create signal generator
    gen = SignalGenerator(t)
    
    # Create x(t) = Square(t) + Triangle(t)
    # Using amplitude=1 and frequency=1 for both signals
    composite = CompositeSignal(t)
    composite.add_component(gen.square(1, 1))
    composite.add_component(gen.triangle(1, 1))
    
    # Get x(t) values
    x_t = composite.values()
    
    # Parameters
    f0 = 10  # Phase shift frequency (modulation frequency)
    a = 10   # Time compression factor
    
    # Create y(t) = x(at) * e^(j2πf₀t)
    # This involves:
    # i. Time compression: x(at)
    # ii. Phase shift (modulation): multiply by e^(j2πf₀t)
    
    # For x(at), we need to evaluate x at scaled time points
    # Create a new generator for the scaled signal
    gen_scaled = SignalGenerator(a * t)  # t_scaled = a*t
    x_at = gen_scaled.square(1, 1) + gen_scaled.triangle(1, 1)
    
    # Apply phase shift: y(t) = x(at) * e^(j2πf₀t)
    # e^(j2πf₀t) = cos(2πf₀t) + j*sin(2πf₀t)
    y_real = x_at * np.cos(2 * np.pi * f0 * t)
    y_imag = x_at * np.sin(2 * np.pi * f0 * t)
    
    # Define frequency axis: f ∈ [-10, 10] with at least 1000 samples
    frequencies = np.linspace(-10, 10, 1000)
    
    # Compute CFT of x(t)
    cft_x = CFTAnalyzer(composite, t, frequencies)
    X_a, X_b = cft_x.compute_cft()
    
    # Compute magnitude and phase of X(f)
    X_mag = np.sqrt(X_a**2 + X_b**2)
    X_phase = np.arctan2(X_b, X_a)
    
    # Compute CFT of y(t) (complex signal)
    cft_y = ComplexCFTAnalyzer(y_real, y_imag, t, frequencies)
    Y_a, Y_b = cft_y.compute_cft()
    
    # Compute magnitude and phase of Y(f)
    Y_mag = np.sqrt(Y_a**2 + Y_b**2)
    Y_phase = np.arctan2(Y_b, Y_a)
    
    # Theoretical prediction: Y(f) = (1/|a|) * X((f-f₀)/a)
    # Compute X at shifted and scaled frequencies: (f-f₀)/a
    f_shifted_scaled = (frequencies - f0) / a
    
    # Interpolate X at these frequencies
    X_a_interp = np.interp(f_shifted_scaled, frequencies, X_a, left=0, right=0)
    X_b_interp = np.interp(f_shifted_scaled, frequencies, X_b, left=0, right=0)
    
    # Compute predicted magnitude and phase
    X_mag_predicted = np.sqrt(X_a_interp**2 + X_b_interp**2) / abs(a)
    X_phase_predicted = np.arctan2(X_b_interp, X_a_interp)
    
    # =====================================================
    # Numerical Verification - Plotting
    # =====================================================
    
    # Plot original signal x(t)
    plt.figure(figsize=(14, 10))
    
    plt.subplot(3, 2, 1)
    plt.plot(t, x_t)
    plt.xlabel("Time (t)")
    plt.ylabel("Amplitude")
    plt.title("Original Signal: x(t) = Square(t) + Triangle(t)")
    plt.grid(True)
    
    # Plot modified signal y(t) - real part
    plt.subplot(3, 2, 2)
    plt.plot(t, y_real, label='Real part')
    plt.plot(t, y_imag, label='Imaginary part', alpha=0.7)
    plt.xlabel("Time (t)")
    plt.ylabel("Amplitude")
    plt.title("Modified Signal: y(t) = x(10t) * $e^{j2\pi f_0 t}$")
    plt.legend()
    plt.grid(True)
    
    # Plot magnitude comparison
    plt.subplot(3, 2, 3)
    plt.plot(frequencies, Y_mag, label='|Y(f)|', linewidth=2)
    plt.plot(frequencies, X_mag_predicted, '--', label='$\\frac{1}{|a|} |X(\\frac{f-f_0}{a})|$', linewidth=2)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Magnitude Spectrum Comparison")
    plt.legend()
    plt.grid(True)
    
    # Plot phase comparison
    plt.subplot(3, 2, 4)
    plt.plot(frequencies, Y_phase, label='∠Y(f)', linewidth=2)
    plt.plot(frequencies, X_phase_predicted, '--', label='∠X($\\frac{f-f_0}{a}$)', linewidth=2)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (radians)")
    plt.title("Phase Spectrum Comparison")
    plt.legend()
    plt.grid(True)
    
    # Plot magnitude error
    plt.subplot(3, 2, 5)
    mag_error = Y_mag - X_mag_predicted
    plt.plot(frequencies, mag_error)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Error")
    plt.title("Magnitude Error: |Y(f)| - $\\frac{1}{|a|} |X(\\frac{f-f_0}{a})|$")
    plt.grid(True)
    
    # Plot phase error
    plt.subplot(3, 2, 6)
    # Handle phase wrapping for error calculation
    phase_error = np.angle(np.exp(1j * (Y_phase - X_phase_predicted)))
    plt.plot(frequencies, phase_error)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Error (radians)")
    plt.title("Phase Error: ∠Y(f) - ∠X($\\frac{f-f_0}{a}$)")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # =====================================================
    # Error Analysis
    # =====================================================
    
    # MSE for magnitude
    mse_magnitude = np.mean((Y_mag - X_mag_predicted)**2)
    
    # MSE for phase (considering phase wrapping)
    phase_diff = np.angle(np.exp(1j * (Y_phase - X_phase_predicted)))
    mse_phase = np.mean(phase_diff**2)
    
    print("\n" + "="*60)
    print("ERROR ANALYSIS")
    print("="*60)
    print(f"MSE (Magnitude): {mse_magnitude:.10e}")
    print(f"MSE (Phase):     {mse_phase:.10e}")
    print("="*60)
    
    # Check if within tolerance
    tolerance = 1e-5
    if mse_magnitude < tolerance and mse_phase < tolerance:
        print("✓ Both MSE values are within acceptable tolerance.")
        print(f"  Magnitude: {mse_magnitude:.2e} < {tolerance}")
        print(f"  Phase:     {mse_phase:.2e} < {tolerance}")
    else:
        print("⚠ MSE values may be outside typical tolerance.")
    
    print("\n" + "="*60)
    print("FOURIER TRANSFORM PROPERTIES VERIFICATION")
    print("="*60)
    print("Theoretical Relationship:")
    print("  y(t) = x(at) * e^(j2πf₀t)")
    print("  Y(f) = (1/|a|) * X((f-f₀)/a)")
    print(f"\nParameters:")
    print(f"  Time compression factor (a): {a}")
    print(f"  Modulation frequency (f₀):  {f0} Hz")
    print("\nEffects:")
    print("  (i) Phase shift (modulation): Shifts spectrum in frequency domain by f₀")
    print("  (ii) Time compression: Expands spectrum by factor 'a' and scales amplitude by 1/|a|")
    print("="*60)

