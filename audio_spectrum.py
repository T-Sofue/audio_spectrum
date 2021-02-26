import pyaudio
import numpy as np
import time
import matplotlib.pyplot as plt
import scipy

def fft(samples,sample_rate):
    n=len(samples)
    t=1/sample_rate
    yf = scipy.fft.fft(samples)
    #yf[ yf == 0 ] = 1
    freq = np.linspace(0,int(1/(2*t)),int(n/2))
    mag = 2/n*np.abs(yf[:n//2])
    return mag,freq,yf

mic = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
stream = mic.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

x = [i for i in range(CHUNK)]
y = [100 for i in range(CHUNK)]

fig, ax = plt.subplots(figsize=(14,6))
ax.grid()
plt.xlabel("Freq (Hz)")
plt.ylabel("Magnitude")
x = np.arange(0, 2 * CHUNK, 2)
ax.set_ylim(0, 1000)
ax.set_xlim(20,4000)
line, = ax.plot(x,y)

while True:
    data = stream.read(CHUNK,exception_on_overflow = False)
    data = np.frombuffer(data, np.int16)
    mag,freq,_ = fft(data,RATE)
    line.set_ydata(mag)
    line.set_xdata(freq)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.001)

stream.stop_stream()
stream.close()
p.terminate()

#print(frames)
