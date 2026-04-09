import numpy as np
import matplotlib.pyplot as plt

class SmartIrrigation:
    def __init__(self, a=0.5, b=1.0, t_max=20, dt=0.01):
        self.a = float(a)
        self.b = float(b)
        self.t_max = float(t_max)
        self.dt = float(dt)
        self.t = np.arange(0.0, self.t_max + self.dt, self.dt)

    def u_step(self):
        return np.ones_like(self.t)

    def u_ramp(self):
        return 0.1 * self.t

    def u_sin(self):
        return np.sin(0.5 * self.t)

    def u_exponential(self): 
        return 1.0 - np.exp(-0.3 * self.t)

    def u_pulse(self):
        return np.where(self.t < 5.0, 1.0, 0.0)

    def laplace_transform(self, f, s):
        return np.trapezoid(f * np.exp(-s * self.t), self.t)

    def inverse_laplace(self, s_list, F_s_values):
        dw = np.abs(np.imag(s_list[1] - s_list[0]))

        h = np.zeros_like(self.t, dtype=float)
        for i, ti in enumerate(self.t):
            h[i] = (dw / (2.0 * np.pi)) * np.real(np.sum(F_s_values * np.exp(s_list * ti)))
        return h

    def H_s(self, s, U_s):
        return (self.b / (s + self.a)) * U_s

    def steady_state(self, h):
        """Mean of last 5% of signal."""
        idx = int(np.ceil(0.05 * len(h)))
        return float(np.mean(h[-idx:]))

    def time_constant(self, h):
        """Time to first reach 63.2% of steady-state."""
        h_ss = self.steady_state(h)

        first = 0.632 * h_ss
        if h_ss > 0:
            idx = np.where(h >= first)[0]
        else:
            idx = np.where(h <= first)[0]

        return float(self.t[idx[0]]) if idx.size else np.nan

    def rise_time(self, h):
        """Time to go from 10% to 90% of steady-state."""
        h_ss = self.steady_state(h)

        if h_ss > 0:
            ih_l = np.where(h >= (0.1* h_ss))[0]
            ih_h = np.where(h >= (0.9* h_ss))[0]
        else:
            ih_l = np.where(h <= (0.1* h_ss))[0]
            ih_h = np.where(h <= (0.1* h_ss))[0]

        return float(self.t[ih_h[0]] - self.t[ih_l[0]])

    def settling_time(self, h):
        """Time after which h(t) stays permanently within ±2% of h_ss."""
        h_ss = self.steady_state(h)
        rg = 0.02 * abs(h_ss)

        for i in range(len(h)):
            if np.all(np.abs(h[i:] - h_ss) <= rg):
                return self.t[i]

    def overshoot(self, h):
        """Percentage overshoot: (h_max - h_ss) / h_ss * 100."""
        h_ss = self.steady_state(h)

        h_max = np.max(h)
        tar = ((h_max - h_ss) / abs(h_ss)) * 100.0
        return float(max(0.0, tar))

    def compute_metrics(self, h):
       
        return {
            "steady_state":  self.steady_state(h),
            "time_constant": self.time_constant(h),
            "rise_time":     self.rise_time(h),
            "settling_time": self.settling_time(h),
            "overshoot_%":   self.overshoot(h),
        }

    def euler_simulate(self, u):
        """
        Euler method for dh/dt = -a*h(t) + b*u(t)
        h[n+1] = h[n] + dt * (-a*h[n] + b*u[n])
        """
        h = np.zeros_like(self.t)
        for n in range(len(self.t) - 1):
            dhdt = -self.a * h[n] + self.b * u[n]
            h[n + 1] = h[n] + self.dt * dhdt
        return h


#Change values of a, b to experiment with different system dynamics
system = SmartIrrigation(a=0.5, b=1.0, t_max=20, dt=0.01)

inputs = {
    "Step Input":        system.u_step(),
    "Ramp Input":        system.u_ramp(),
    "Sinusoidal Input":  system.u_sin(),
    "Exponential Input": system.u_exponential(),
    "Pulse Input":       system.u_pulse(),
}

# Bromwich contour parameters, set these values
c = 0.5
W = 100.0
N = 5000
w = np.linspace(-W, W, N)
s_list = c + 1j * w

colors = ['#2196F3', '#4CAF50', '#FF5722', '#9C27B0', '#FF9800']

for idx, (name, u) in enumerate(inputs.items()):
    print(f"Processing: {name}...")

    # --- Laplace --- set these values
    U_s_vals = np.array([system.laplace_transform(u, s) for s in s_list])
    H_s_vals = system.H_s(s_list, U_s_vals)
    h_laplace = system.inverse_laplace(s_list, H_s_vals)
    print(f"\n  ► {name}")
    metrics = system.compute_metrics(h_laplace)
    for k, v in metrics.items():
        print(f"      {k.replace('_',' ').title():<22}: {v}")

    # --- Euler ---
    h_euler = system.euler_simulate(u)

    # --- Plot ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=False)
    fig.suptitle(f"Smart Irrigation — {name}", fontsize=13, fontweight='bold')

    # Laplace subplot
    axes[0].plot(system.t, u, 'b--', lw=1.8, label="Input u(t)")
    axes[0].plot(system.t, h_laplace, color=colors[idx], lw=2.2, label="Output h(t)")
    axes[0].set_title("Laplace Transform Simulation", fontweight='bold')
    axes[0].set_xlabel("Time (s)", fontsize=11)
    axes[0].set_ylabel("Water Level / Input", fontsize=11)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)

    # Euler subplot
    axes[1].plot(system.t, u, 'b--', lw=1.8, label="Input u(t)")
    axes[1].plot(system.t, h_euler, color='tomato', lw=2.2, label="Output h(t)")
    axes[1].set_title("Euler Method Simulation", fontweight='bold')
    axes[1].set_xlabel("Time (s)", fontsize=11)
    axes[1].set_ylabel("Water Level / Input", fontsize=11)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()