import numpy as np

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