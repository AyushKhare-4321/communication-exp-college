import numpy as np
import matplotlib.pyplot as	plt
from scipy.signal import square
import matplotlib as mpl


plt.style.use('fivethirtyeight')
mpl.rcParams['lines.linewidth'] = 2.0
mpl.rcParams['figure.facecolor'] = "white"
mpl.rcParams['axes.facecolor'] = "white"

fs = 100 	# sampling frequency
Ts = 1 / fs # sampling interval
t = np.arange(0, 1, Ts)

# Generation of three message signals
messages = [
	2 * np.sin(2 * np.pi * 3 * t),
	1 * square(2 * np.pi * 3 * t),
	3 * np.cos(2 * np.pi * 7 * t)
]
titles = ["Sine wave", "Square wave", "Cosine wave"]
fig, axs = plt.subplots(3, 1, sharex=True, layout="constrained")
for i in range(3):
	axs[i].stem(t, messages[i], markerfmt="")
	axs[i].grid(False)
	axs[i].set(
		ylabel="Amplitude", 
		title=f"Message signal {i+1} ({titles[i]})")
axs[i].set_xlabel("Time (s)")

# Generation of Time Division Multiplexing Signal
tdm = np.zeros(len(messages) * len(t))
tdm[0::3] = messages[0]
tdm[1::3] = messages[1]
tdm[2::3] = messages[2]
fig, ax = plt.subplots(layout="constrained")
ax.stem(tdm, markerfmt="")
ax.set(xlabel="Time (s)", ylabel="Amplitude",
		title="Time Division Multiplixed Signal")

# Demultiplexing of TDM signal
demultiplexed_message = [tdm[i::3] for i in range(len(messages))]

fig, axs = plt.subplots(3, 1, sharex=True, layout="constrained")
for i in range(3):
	axs[i].stem(t, demultiplexed_message[i], markerfmt="")
	axs[i].grid(False)
	axs[i].set(
		ylabel="Amplitude", 
		title=f"Demux Message signal {i+1} ({titles[i]})")
axs[i].set_xlabel("Time (s)")

plt.show()