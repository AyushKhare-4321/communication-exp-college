import numpy as np
import matplotlib.pyplot as plt
from math import ceil
import matplotlib as mpl


plt.style.use('ggplot')
mpl.rcParams['lines.linewidth'] = 2.0
mpl.rcParams['figure.facecolor'] = "None"
mpl.rcParams['axes.facecolor'] = "None"
mpl.rcParams['grid.color'] = "k"
mpl.rcParams['grid.alpha'] = 0.5

def get_mag_spectrum(x):
	N = len(x)
	magnitude = 2 * np.abs(np.fft.fft(x)) / N
	magnitude[0] = magnitude[0] / 2
	frequencies = np.fft.fftfreq(N, d=Ts)
	return frequencies, magnitude

def apply_lowpass_filter(signal, cutoff):
	k = np.abs(np.fft.fft(signal))
	k[cutoff:] = 0
	return np.fft.ifft(k).real

fm = 3
fc = 20
fs = 500 	# sampling frequency
Ts = 1 / fs # sampling interval
t = np.arange(0, 3, 1 / fs)
N = len(t)
am = 2
ac = 4 

# Modulation
message = am * np.cos(2 * np.pi * fm * t)
carrier = ac * np.cos(2 * np.pi * fc * t)
ka = 1 / ac
mu = ka * am
modulated_wave = (1 + ka * message) * carrier
print(f"Modulation index: {mu:.2f}")

fig, axs = plt.subplots(3, 1, sharex=True, layout="constrained")
for ax in axs.flatten():
	ax.set_ylabel("Amplitude")

axs[0].plot(t, message)
axs[0].set_title("Message Signal")

axs[1].plot(t, carrier)
axs[1].set_title("Carrier Signal")

axs[2].plot(t, modulated_wave)
axs[2].set_title("Amplitude Modulated Signal")
axs[2].set_xlabel("Time (s)")


# Frequency Spectrum
fig, axs = plt.subplots(2, 1, layout="constrained")
axs[0].stem(*get_mag_spectrum(modulated_wave), markerfmt="")
axs[0].set_xlabel("Frequency (Hz)")
axs[0].set_ylabel("Amplitude")
axs[0].set_title("AM Signal Spectrum")
axs[0].set_xlim(-40, 40)

# Demodulation of AM signal
demodulated_wave = modulated_wave * carrier
axs[1].plot(t, apply_lowpass_filter(demodulated_wave, 4*fm))
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Amplitude")
axs[1].set_title("Demodulated Message")

plt.show()