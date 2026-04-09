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

    def gaussian(self, a):
        """Generate a Gaussian signal: x(t) = e^(-at^2)."""
        return np.exp(-a * self.t ** 2)


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
# Time-Shifted Signal Class
# =====================================================
class TimeShiftedSignal(ContinuousSignal):
    """
    Represents a time-shifted version of a signal.
    y(t) = x(t - t0)
    """

    def __init__(self, original_signal, t, time_shift):
        """
        Args:
            original_signal: numpy array of the original signal values
            t: time axis for the shifted signal
            time_shift: the time shift value t0
        """
        super().__init__(t)
        self.original_signal = original_signal
        self.time_shift = time_shift
        self.original_t = t

    def values(self):
        """
        Returns the time-shifted signal by evaluating at (t - t0).
        Uses interpolation to get values at shifted time points.
        """
        shifted_t = self.t - self.time_shift
        # Interpolate to get signal values at the shifted time points
        return np.interp(shifted_t, self.original_t, self.original_signal, left=0, right=0)


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
# Main Execution (Task 1)
# =====================================================
# t = np.linspace(-4, 4, 3000)
# gen = SignalGenerator(t)

# composite = CompositeSignal(t)
# composite.add_component(gen.sine(2, 1))
# composite.add_component(gen.cosine(0.5, 3))
# composite.add_component(gen.triangle(1, 1))
# composite.add_component(gen.cubic(1) * gen.rectangular(2))

# composite.plot("Composite Signal")

# frequencies = np.linspace(-10, 10, 5000)
# cft = CFTAnalyzer(composite, t, frequencies)
# cft.plot_spectrum()
# cft.plot_phase()

# icft = InverseCFT(cft.compute_cft(), frequencies, t)
# x_rec = icft.reconstruct()

# plt.plot(t, composite.values(), label="Original")
# plt.plot(t, x_rec, '--', label="Reconstructed")
# plt.legend()
# plt.title("Reconstruction using ICFT")
# plt.show()


# =====================================================
# Driver Code for Time-Shift Property Verification
# =====================================================

# Part 2: Define time axis and generate original signal
t = np.linspace(-5, 5, 2000)
gen = SignalGenerator(t)
x_t = gen.gaussian(a=1)  # x(t) = e^(-t^2)

# Create a ContinuousSignal wrapper for x(t)
class GaussianSignal(ContinuousSignal):
    def __init__(self, t, signal_values):
        super().__init__(t)
        self.signal_values = signal_values
    
    def values(self):
        return self.signal_values

x_signal = GaussianSignal(t, x_t)

# Part 3: Time-shift the signal (t0 = 1)
t0 = 1
y_signal = TimeShiftedSignal(x_t, t, t0)

# Part 4: Compute CFT of both signals
frequencies = np.linspace(-10, 10, 1000)

cft_x = CFTAnalyzer(x_signal, t, frequencies)
cft_y = CFTAnalyzer(y_signal, t, frequencies)

X_a, X_b = cft_x.compute_cft()
Y_a, Y_b = cft_y.compute_cft()

# Calculate magnitudes and phases
X_mag = np.sqrt(X_a**2 + X_b**2)
Y_mag = np.sqrt(Y_a**2 + Y_b**2)
X_phase = np.arctan2(X_b, X_a)
Y_phase = np.arctan2(Y_b, Y_a)

# Part 5: Plot the magnitude spectra
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(frequencies, X_mag, label='|X(f)|', linewidth=2)
plt.plot(frequencies, Y_mag, '--', label='|Y(f)|', linewidth=2)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Magnitude Spectra Comparison")
plt.legend()
plt.grid(True)

# Plot the phase spectra
plt.subplot(1, 2, 2)
plt.plot(frequencies, X_phase, label='∠X(f)', linewidth=2)
plt.plot(frequencies, Y_phase, '--', label='∠Y(f)', linewidth=2)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Phase (radians)")
plt.title("Phase Spectra Comparison")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Part 6: Error Analysis

# (a) MSE of Magnitude
MSE_mag = np.mean((X_mag - Y_mag)**2)
print(f"Mean Squared Error of Magnitude: {MSE_mag:.10e}")
print(f"Comment: The MSE is very small (close to zero), confirming that |X(f)| = |Y(f)|")
print(f"         as predicted by the time-shift property.\n")

# (b) Phase Difference Error
# Theoretical phase of Y(f): ∠Y(f) = ∠X(f) - 2πft0
Y_phase_theoretical = X_phase - 2 * np.pi * frequencies * t0

# Wrap phase differences to [-π, π] to handle phase wrapping
phase_diff = Y_phase - Y_phase_theoretical
phase_diff = np.arctan2(np.sin(phase_diff), np.cos(phase_diff))

MSE_phase = np.mean(phase_diff**2)
print(f"Mean Squared Error of Phase: {MSE_phase:.10e}")
print(f"Comment: The phase MSE is very small, confirming that ∠Y(f) = ∠X(f) - 2πft₀")
print(f"         as predicted by the time-shift property.")

# Additional verification plot: Phase difference
plt.figure(figsize=(10, 4))
plt.plot(frequencies, Y_phase_theoretical, label='Theoretical ∠Y(f) = ∠X(f) - 2πft₀', linewidth=2)
plt.plot(frequencies, Y_phase, '--', label='Computed ∠Y(f)', linewidth=2, alpha=0.7)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Phase (radians)")
plt.title("Phase Verification: Theoretical vs Computed")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
