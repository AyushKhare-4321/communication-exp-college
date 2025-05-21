import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.signal import hilbert

# print(plt.style.available)
# print(mpl.rcParams.keys())
# plt.style.use("fivethirtyeight")
# mpl.rcParams["lines.linewidth"] = 2
# mpl.rcParams["axes.facecolor"] = "None"
# mpl.rcParams["axes.grid"] = True
# mpl.rcParams["figure.facecolor"] = "None"

fs = 50 	# sampling frequency
Ts = 1 / fs # sampling interval
t = np.arange(0, 2, Ts)
N = len(t)

fm = 2
fc = 20
am = 2 
ac = 3

message = am * np.cos(2 * np.pi * fm * t)
carrier = ac * np.cos(2 * np.pi * fc * t)
# Hilbert transforms
h_message = np.imag(hilbert(message))
h_carrier = np.imag(hilbert(carrier))

fig, axs = plt.subplots(2, 1, sharex=True, layout="constrained")
axs = axs.flatten()

axs[0].plot(t, message,  label="Message")
axs[0].plot(t, h_message, "--", label="Message Hilbert")
axs[0].set_title("Message Signal")

axs[1].plot(t, carrier, label="Carrier")
axs[1].plot(t, h_carrier, "--", label="Carrier Hilbert")
axs[1].set_title("Carrier Signal")
axs[1].set_xlabel("Time (s)")
axs[1].set_xlim(0, .5)
for ax in axs:
	ax.set_ylabel("Amplitude")
	ax.legend(loc="upper right")
	ax.grid(True)

# Single side band supressed carrier modulation
# lower side band
ssbsc_lsb = message * carrier + h_message * h_carrier
# upper side band
ssbsc_usb = message * carrier - h_message * h_carrier

# frequency spectrum
# LSB
def get_freq_spectrum(x):
	N = len(x)
	magnitude = 2 * np.abs(np.fft.fft(x)) / N
	magnitude[0] = magnitude[0] / 2
	frequencies = np.fft.fftfreq(N, d=Ts)
	return frequencies, magnitude

def plot_freq_spectrum(signal, title, ax):
	ax.stem(*get_freq_spectrum(signal), markerfmt="", basefmt="k")
	ax.set_title(title)
	ax.set_ylabel("Amplitude")
	ax.grid(True)

fig, axs = plt.subplots(3, 1, layout="constrained", sharex=False)
plot_freq_spectrum(ssbsc_lsb, "SSB Modulated Signal (LSB)", axs[0])
plot_freq_spectrum(ssbsc_usb, "SSB Modulated Signal (USB)", axs[1])
axs[1].set_xlabel("Frequency (Hz)")

# SSB demodulation
demodulated_wave = ssbsc_lsb * carrier
def apply_lowpass_filter(signal, cutoff):
	k = np.abs(np.fft.fft(signal))
	k[cutoff:] = 0
	return np.fft.ifft(k).real
axs[2].plot(t, apply_lowpass_filter(demodulated_wave, 3*fm))
axs[2].set_title("Demodulated Message")
axs[2].set_xlabel("Time (s)")
axs[2].set_ylabel("Amplitude")
axs[2].grid(True)
plt.show()