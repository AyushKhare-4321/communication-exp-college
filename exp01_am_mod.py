import numpy as np
import matplotlib.pyplot as plt
from math import ceil
import matplotlib as mpl

plt.style.use('ggplot')

mpl.rcParams['lines.linewidth'] = 2.0

def fft_magnitude_onesided(x, fs):
	N = len(x)
	fft_idx = np.linspace(0, fs / 2, N // 2)

	fft = np.fft.fft(x)
	# x is real signal
	fft_onesided = fft[:N // 2]
	fft_abs = np.abs(fft_onesided)
	fft_normalized = 2 * fft_abs / N
	# DC value not multilpied by 2
	fft_normalized[0] = fft_normalized[0] / 2
	return fft_idx, fft_normalized

def fft_magnitude_twosided(x, fs):
	N = len(x)
	fft_idx = np.linspace(0, fs, N)
	# second half of FFT is negtive values of f in decreasing order (-ve to 0)
	fft_idx[ceil(N / 2):] = np.linspace(-fs / 2, 0, N // 2)

	fft = np.fft.fft(x)
	fft_abs = np.abs(fft)
	fft_normalized = 2 * fft_abs / N
	# DC value not multilpied by 2
	fft_normalized[0] = fft_normalized[0] / 2
	return fft_idx, fft_normalized



fm = 3
fc = 20
# sampling frequency
fs = 1000
# sampling interval
Ts = 1 / fs
t = np.arange(0, 3, 1 / fs)

am = 2
ac = 4 

message = am * np.cos(2*np.pi*fm*t)
carrier = ac * np.cos(2*np.pi*fc*t)
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


# titles = ["Message Signal", "Carrier Signal", "Amplitude Modulated Signal"]
# signals = (message, carrier, modulated_wave)
# for title, signal, ax in zip(titles, signals, axs.flat):
# 	ax.plot(t, signal)
# 	ax.set_title(title)
# 	ax.set_ylabel("Amplitude")



# Frequency Spectrum
fig, axs = plt.subplots(2, 1, layout="constrained")

N = len(modulated_wave)
magnitude = 2 * np.abs(np.fft.fft(modulated_wave)) / N
# DC value should not be multiplied by 2
magnitude[0] = magnitude[0] / 2
frequencies = np.fft.fftfreq(len(modulated_wave), d=1/fs)

# ax.stem(*fft_magnitude_onesided(modulated_wave, fs), markerfmt="")
# oneside = len(frequencies) // 2
axs[0].stem(frequencies, magnitude, markerfmt="")
axs[0].set_xlabel("Frequency (Hz)")
axs[0].set_ylabel("Amplitude")
axs[0].set_title("AM Signal Spectrum")
axs[0].set_xlim(-40, 40)

# Demodulation of AM signal
demodulated_wave = modulated_wave * carrier
k = np.abs(np.fft.fft(demodulated_wave)) 
# Apply filter (low pass)
k[4 * fm:] = 0
# filt = np.zeros_like(demodulated_wave)
# filt[:4*fm] = 1
# out = filt * k



axs[1].plot(t, np.fft.ifft(k).real)
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Amplitude")
axs[1].set_title("Demodulated Message")


plt.show()