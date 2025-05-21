import numpy as np
import matplotlib.pyplot as	plt
import matplotlib as mpl


plt.style.use('fivethirtyeight')
mpl.rcParams['lines.linewidth'] = 2.0


fs = 1000 	# sampling frequency
Ts = 1 / fs # sampling interval
t = np.arange(0, 3, Ts)
N = len(t)
fm = 3
fc = 20
am = 1
ac = 2

message = am * np.cos(2 * np.pi * fm * t)
carrier = ac * np.cos(2 * np.pi * fc * t)
dsbsc = message * carrier

fig, axs = plt.subplots(3, 1, sharex=True, layout="constrained")
for ax in axs.flatten():
	ax.set_ylabel("Amplitude")

axs[0].plot(t, message)
axs[0].set_title("Message Signal")

axs[1].plot(t, carrier)
axs[1].set_title("Carrier Signal")

axs[2].plot(t, dsbsc)
axs[2].set_title("Amplitude Modulated Signal")
axs[2].set_xlabel("Time (s)")

# Frequency spectrum
fig, axs = plt.subplots(2, 1, layout="constrained")
magnitude = np.abs(np.fft.fft(dsbsc)) / N * 2
magnitude[0] = magnitude[0] / 2
frequencies = np.fft.fftfreq(N, d=Ts)
oneside = len(frequencies) 
axs[0].stem(frequencies[:oneside], magnitude[:oneside], markerfmt="")
axs[0].set_ylabel("Amplitude")
axs[0].set_xlabel("Frequency (Hz)")
axs[0].set_title("DSBSC Signal Spectrum")
axs[0].set_xlim(-30, 30)

# Demodulation of DSBSC signal
demodulated_wave = dsbsc * carrier
def apply_lowpass_filter(signal, cutoff):
	k = np.abs(np.fft.fft(signal))
	k[cutoff:] = 0
	return np.fft.ifft(k).real
axs[1].plot(t, apply_lowpass_filter(demodulated_wave, 4*fm))
axs[1].set_title("Demodulated Message")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Amplitude")

plt.show()