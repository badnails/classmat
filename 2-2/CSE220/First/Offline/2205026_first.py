import numpy as np
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, INF):
        self.INF = INF
        self.signal = np.zeros(2*INF + 1)

    def set_value_at_time(self, t, value):
        # Set the value at time index t
        if -self.INF<=t<=self.INF:
            self.signal[t + self.INF] = value

    def shift(self, k):
        # Shift the signal and return the resultant signal
        New_Signal = Signal(self.INF)
        New_Signal.signal[:] = self.signal
        if k>0 :
            New_Signal.signal[k:] = New_Signal.signal[:-k]
            New_Signal.signal[:k] = 0
        elif k<0 :
            New_Signal.signal[:k] = New_Signal.signal[-k:]
            New_Signal.signal[k:] = 0
        return New_Signal

    def add(self, other):
        # Add two signals and return the resultant signal
        y = Signal(self.INF)
        y.signal = self.signal + other.signal
        return y

    def multiply(self, scalar):
        # Multiply a constant value with the signal
        y = Signal(self.INF)
        y.signal = self.signal * scalar
        return y

    def plot(self, title="No Title Provided"):
        # Plot the signal
        plt.figure(figsize=(8,4))
        plt.stem(np.arange(-self.INF, self.INF+1), self.signal)
        plt.xlabel("idx")
        plt.ylabel("amp")
        plt.title(title)
        plt.grid(True)
        filename = title.replace(" ", "_") + ".png"
        plt.savefig(title.replace(" ", "_")+".png")
        print(f"Plot saved as {filename}")

class LTI_System:
    def __init__(self, impulse_response: Signal):
        # Initialize
        self.impulse_response = impulse_response

    def linear_combination_of_impulses(self, input_signal: Signal):
        # Decompose the signal into impulses and corresponding coefficients
        imp = []
        coeff = []

        for i, amp in enumerate(input_signal.signal):
            if amp != 0:
                impulse_signal = Signal(input_signal.INF)
                impulse_signal.set_value_at_time(i-input_signal.INF, 1)
                
                coeff.append(amp)
                imp.append(impulse_signal)
        return imp, coeff


    def output(self, input_signal: Signal):
        # Calculate and return the output signal
        impulses, coefficients = self.linear_combination_of_impulses(input_signal)
        out = Signal(input_signal.INF)
        for imp, coeff in zip(impulses, coefficients):
            shift_amt = np.argmax(imp.signal) - imp.INF
            temp_shift = self.impulse_response.shift(shift_amt)
            temp_scale = temp_shift.multiply(coeff)
            out = out.add(temp_scale)
        return out


if __name__ == "__main__":
    INF = 10

    # Input signal x(n)
    x = Signal(INF)
    x.set_value_at_time(-2, 1)
    x.set_value_at_time(0, 2)
    x.set_value_at_time(3, -1)

    x.plot("Input Signal x(n)")

    # Impulse response h(n)
    h = Signal(INF)
    h.set_value_at_time(0, 1)
    h.set_value_at_time(1, 0.5)

    h.plot("Impulse Response h(n)")

    # LTI System
    system = LTI_System(h)

    # Output
    y = system.output(x)
    y.plot("Output Signal y(n)")
