import numpy as np
import matplotlib.pyplot as	plt
from scipy.signal import square
from numpy.fft import fft, ifft
import matplotlib as mpl


plt.style.use('fivethirtyeight')
mpl.rcParams['lines.linewidth'] = 2.0
mpl.rcParams['figure.facecolor'] = "white"
mpl.rcParams['axes.facecolor'] = "white"

# Random binary input
n = np.array([0, 1, 0, 1, 0, 0])
polar_bits = np.where(n == 0, -1, 1)

# Generating NRZ waveform from bit sequence of bit duration 1 sec
t = np.arange(0, len(n) + 0.01, 0.01)
carrier = np.sin(2 * np.pi * 4 * t)
data = np.zeros_like(t)
for j in range(len(polar_bits)):
	idx = np.where((j <= t) & (t < j + 1))[0]
	data[idx] = polar_bits[j]

# Amplitude shift keying signal generation
ask = np.where(data == 1, carrier, 0)

fig, axs = plt.subplots(3, 1, layout="constrained", sharex=True)
axs[0].plot(t, data)
axs[0].set(ylabel="Amplitude", title="Binary Input")
axs[1].plot(t, carrier)
axs[1].set(ylabel="Amplitude", title="Carrier Signal")
axs[2].plot(t, ask)
axs[2].set(ylabel="Amplitude", title="Amplitude Shift Keying Signal")
axs[2].set_xlabel("Time (s)")

# Demodulation of ASK signal
demodulated_wave = np.where(ask == carrier, 1, 0)
fig, axs = plt.subplots(3, 1, layout="constrained")
axs[0].plot(t, demodulated_wave)
axs[0].set(xlabel="Time (s)", ylabel="Amplitude", title="Demodulated Message Signal")

plt.show()

