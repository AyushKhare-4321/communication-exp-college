import numpy as np
import matplotlib.pyplot as	plt
from scipy.signal import square
from numpy.fft import fft, ifft
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

fs = 100 	# sampling frequency
Ts = 1 / fs # sampling interval
t = np.arange(0, 2, Ts)

# Generation of two message signals
messages = [
	2 * np.cos(2 * np.pi * 2 * t),
	1 * np.cos(2 * np.pi * 9 * t),
]
N = len(messages)
fig, axs = plt.subplots(N, 1, sharex=True, layout="constrained")
for i in range(N):
	axs[i].plot(t, messages[i])
	axs[i].set(
		ylabel="Amplitude", 
		title=f"Message signal {i+1}")
axs[i].set_xlabel("Time (s)")

# Frequency response
fig, axs = plt.subplots(N+1, 1, layout="constrained")
message_freqs = []
for i in range(N): 
	f, magnitude = get_mag_spectrum(messages[i])
	message_freqs.append(fft(messages[i]))
	axs[i].plot(f, magnitude)
	axs[i].set(ylabel="Magnitude",
				title=f"Spectrum of signal {i+1}")

# Frequency multiplexing
freq_response = sum(message_freqs)
axs[N].plot(f, np.real(freq_response))
axs[N].set(xlabel="Frequency", ylabel="Magnitude",
				title="Frequency Division Multiplixed Signal")

# Frequency demultiplexing
fig, axs = plt.subplots(N, 1, layout="constrained")
filters = [
	np.concatenate([np.ones(10), np.zeros(180), np.ones(10)]),
	np.concatenate([np.zeros(10), np.ones(180), np.zeros(10)]),
]
demod_messages = [ifft(freq_response * filters[i]) for i in range(N)]
for i in range(N):
	axs[i].plot(t, np.real(demod_messages[i]))
	axs[i].set(ylabel="Amplitude", title=f"Recovered Signal {i+1}")
axs[i].set_xlabel("Time (s)")
plt.show()