import numpy as np
import matplotlib.pyplot as	plt
from scipy.signal import square
import matplotlib as mpl


plt.style.use('fivethirtyeight')
mpl.rcParams['lines.linewidth'] = 2.0
mpl.rcParams['figure.facecolor'] = "white"
mpl.rcParams['axes.facecolor'] = "white"

def get_mag_spectrum(x):
	N = len(x)
	magnitude = 2 * np.abs(np.fft.fft(x)) / N
	magnitude[0] = magnitude[0] / 2
	frequencies = np.fft.fftfreq(N, d=Ts)
	return frequencies, magnitude

def apply_lowpass_filter(signal, cutoff):
	k = np.abs(np.fft.fft(signal))
	# _, k = get_mag_spectrum(signal)
	k[cutoff:] = 0
	return np.fft.ifft(k).real

fs = 300 	# sampling frequency
Ts = 1 / fs # sampling interval
t = np.arange(0, 2, Ts)
N = len(t)
fm = 3
fc = 25
am = 3
ac = 5

message = am + am * np.sin(2 * np.pi * fm * t)
carrier = ac + ac * square(2 * np.pi * fc * t)
pam_mod = message * carrier

fig, axs = plt.subplots(3, 1, sharex=True, layout="constrained")
for ax in axs.flatten():
	ax.set_ylabel("Amplitude")

axs[0].plot(t, message)
axs[0].set_title("Message Signal")

axs[1].plot(t, carrier)
axs[1].set_title("Carrier Signal")

axs[2].plot(t, pam_mod)
axs[2].set_title("Pulse Amplitude Modulated Signal")
axs[2].set_xlabel("Time (s)")
axs[2].set_xlim(0, 1.5)

# Demodulation of PAM signal
demodulated_wave = pam_mod * carrier
fig, ax = plt.subplots()
ax.plot(t, apply_lowpass_filter(demodulated_wave, 3*fm))

plt.show()