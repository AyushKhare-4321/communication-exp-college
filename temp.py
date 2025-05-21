import numpy as np 
import matplotlib.pyplot as plt
from math import ceil
from scipy.signal import hilbert

fs = 1000
f = 440
t = np.arange(20, 100, 1 / fs)
x = 50 * np.sin(2 * np.pi * f * t) + 10

plt.style.use("ggplot")

def is_even(x): return x % 2 == 0

def get_fft(t, x, fs):
	N = len(t)
	fft_idx = np.linspace(0, fs, N)
 
	fft = np.fft.fft(x)
	fft = fft[:len(fft_idx)]
	fftshift = np.fft.fftshift(fft)
	if is_even(N):
		fft_idx[N // 2:] = np.linspace(-fs / 2, 0, N // 2)
	return fft_idx, np.abs(fft)

def get_fft_magnitude_onesided(x, fs):
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

def get_fft_magnitude_twosided(x, fs):
	N = len(x)
	fft_idx = np.linspace(0, fs, N)
	fft_idx[ceil(N / 2):] = np.linspace(-fs / 2, 0, N // 2)

	fft = np.fft.fft(x)
	fft_abs = np.abs(fft)
	fft_normalized = 2 * fft_abs / N
	# DC value not multilpied by 2
	fft_normalized[0] = fft_normalized[0] / 2
	return fft_idx, fft_normalized

# fft_idx = np.linspace(0, fs / 2, len(t) // 2)
# fft = np.fft.fft(x)
# fft_abs = np.abs(fft[:len(fft_idx)])
# fft_shift = np.fft.fftshift(fft)

# # Compute DFT
# fft_result = np.fft.fft(x)
# freqs = np.fft.fftfreq(len(x), d=1/fs)

# # take mag
# magnitude = np.abs(fft_result[:len(t)//2])
# freqs = freqs[:len(t)//2]




# # plt.plot(np.linspace(-fs / 2, fs / 2, len(t)), np.abs(fft_shift) / len(t))
# plt.stem(*get_fft_magnitude_twosided(x,fs), markerfmt="")
# plt.grid(True)
# plt.show()

# -----Parameters-----
fm = 3
fc = 20
# sampling frequency
fs = 500
# sampling interval
Ts = 1 / fs
t = np.arange(0, 3, 1 / fs)

am = 2
ac = 4 

message = am * np.cos(2*np.pi*fm*t)
carrier = ac * np.cos(2*np.pi*fc*t) + np.sin(10 * (fm + fc) * t )
ka = 1 / ac
mu = ka * am
modulated_wave = (1 + ka * message) * carrier


h = hilbert(modulated_wave)
plt.plot(t, modulated_wave)
plt.plot(t, np.abs(h))
plt.show()
print(h.shape)
