import numpy as np
import matplotlib.pyplot as plot

class DiscreteSignal:
    """
    Represents a discrete-time signal.
    """
    def __init__(self, data):
        # Ensure data is a numpy array, potentially complex
        self.data = np.array(data, dtype=np.complex128)

    def __len__(self):
        return len(self.data)
        
    def pad(self, new_length):
        """
        Zero-pad or truncate signal to new_length.
        Returns a new DiscreteSignal object.
        """
        return DiscreteSignal(self.data[:new_length] if new_length<len(self.data) else np.pad(self.data, (0, new_length-len(self.data)), constant_values=0))

    def interpolate(self, new_length):
        """
        Resample signal to new_length using linear interpolation.
        Required for Task 4 (Drawing App).
        """
        # if(new_length<=self.__len__): return self

        return DiscreteSignal(np.interp(np.linspace(0,1,new_length), np.linspace(0,1,len(self.data)), self.data))

        
    def print(self):
        print(self.data)


class DFTAnalyzer:
    """
    Performs Discrete Fourier Transform using O(N^2) method.
    """
    def compute_dft(self, signal: DiscreteSignal):
        """
        Compute DFT using naive summation.
        Returns: numpy array of complex frequency coefficients.
        """
        N = len(signal)
        X = np.zeros(N, dtype=np.complex128)

        for k in range(N):
            for n in range(N):
                X[k] += signal.data[n] * np.exp(-1j * 2 * np.pi * k * n /N)
        
        return X

    def compute_idft(self, spectrum):
        """
        Compute Inverse DFT using naive summation.
        Returns: numpy array (time-domain samples).
        """
        N = len(spectrum)
        x = np.zeros(N, dtype='complex')

        for n in range(N):
            for k in range(N):
                x[n] += spectrum[k] * np.exp(1j * 2 * np.pi * k * n /N)
        
        return x/N


class FastFourierTransform(DFTAnalyzer):
    def base(self, x, invert=False):
        N = len(x)
        if N <= 1: return x
        
        even, odd = self.base(x[::2], invert), self.base(x[1::2], invert)

        sign = 1j if invert else -1j
        twiddles = np.exp(sign * 2 * np.pi * np.arange(N // 2) / N)
        
        combined = twiddles * odd
        return np.concatenate([even + combined, even - combined])

    def compute_dft(self, signal: DiscreteSignal):
        return self.base(np.asarray(signal.data))

    def compute_idft(self, spectrum):
        return self.base(np.asarray(spectrum), invert=True) / len(spectrum)