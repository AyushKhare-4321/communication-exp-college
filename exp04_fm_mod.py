import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

plt.style.use("fivethirtyeight")
mpl.rcParams["lines.linewidth"] = 2
mpl.rcParams["axes.facecolor"] = "None"
mpl.rcParams["figure.facecolor"] = "None"

def get_mag_spectrum(x):
	N = len(x)
	magnitude = 2 * np.abs(np.fft.fft(x)) / N
	magnitude[0] = magnitude[0] / 2
	frequencies = np.fft.fftfreq(N, d=Ts)
	return frequencies, magnitude

fs = 300 	# sampling frequency
Ts = 1 / fs # sampling interval
t = np.arange(0, 3, Ts)
N = len(t)
fm = 2
fc = 23
am = 4
ac = 3

message = am * np.cos(2 * np.pi * fm * t)
carrier = ac * np.cos(2 * np.pi * fc * t)
kf = 4
mod_index = kf * am / fm
fm_mod = ac * np.cos(2 * np.pi * fc * t 
	+ mod_index * np.sin(2 * np.pi * fm * t))


print(f"Modulation index: {mod_index}")
fig, axs = plt.subplots(3, 1, sharex=True, layout="constrained")
for ax in axs.flatten():
	ax.set_ylabel("Amplitude")
	ax.grid(True)

axs[0].plot(t, message)
axs[0].set_title("Message Signal")

axs[1].plot(t, carrier)
axs[1].set_title("Carrier Signal")

axs[2].plot(t, fm_mod)
axs[2].set_title("Frequency Modulated Signal")
axs[2].set_xlabel("Time (s)") 

# Frequency spectrum
fig, ax = plt.subplots(1, figsize=(12, 4))
ax.stem(*get_mag_spectrum(fm_mod), markerfmt="")
ax.set_xlabel("Frequency");
ax.set_ylabel("Amplitude");
ax.set_title("FM Signal Spectrum")
plt.show()