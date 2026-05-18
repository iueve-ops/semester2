import os
import wave

import numpy as np
import matplotlib.pyplot as plt

if not os.path.exists("input.wav"):
    chastota = 44100
    dlina = 5
    vremya = np.linspace(0, dlina, chastota * dlina, False)
    signal = 0.5 * np.sin(2 * np.pi * 220 * vremya)
    signal = signal + 0.3 * np.sin(2 * np.pi * 900 * vremya)
    signal = signal + 0.2 * np.sin(2 * np.pi * 3000 * vremya)
    signal = signal / np.max(np.abs(signal)) * 32767
    signal = signal.astype(np.int16)

    f = wave.open("input.wav", "w")
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(chastota)
    f.writeframes(signal.tobytes())
    f.close()

f = wave.open("input.wav", "r")
kanali = f.getnchannels()
razmer = f.getsampwidth()
chastota = f.getframerate()
kolvo = f.getnframes()
data = f.readframes(kolvo)
f.close()

signal = np.frombuffer(data, dtype=np.int16)

if kanali > 1:
    signal = signal.reshape(-1, kanali)
    signal = signal[:, 0]

signal = signal.astype(float)
vremya = np.arange(len(signal)) / chastota
k = int(chastota * 0.03)

plt.figure()
plt.plot(vremya[:k], signal[:k])
plt.title("Исходный сигнал")
plt.xlabel("Время")
plt.ylabel("Амплитуда")
plt.savefig("signal.png")

fourier = np.fft.rfft(signal)
freq = np.fft.rfftfreq(len(signal), 1 / chastota)

plt.figure()
plt.plot(freq, np.abs(fourier))
plt.xlim(0, 5000)
plt.title("Спектр сигнала")
plt.xlabel("Частота")
plt.ylabel("Сила")
plt.savefig("spectrum.png")

low_fourier = fourier.copy()
low_fourier[freq > 600] = 0
low = np.fft.irfft(low_fourier, n=len(signal))

high_fourier = fourier.copy()
high_fourier[freq < 1000] = 0
high = np.fft.irfft(high_fourier, n=len(signal))

middle_fourier = fourier.copy()
middle_fourier[(freq < 500) | (freq > 1500)] = 0
middle = np.fft.irfft(middle_fourier, n=len(signal))

plt.figure()
plt.subplot(3, 1, 1)
plt.plot(vremya[:k], low[:k])
plt.title("Низкие частоты")
plt.subplot(3, 1, 2)
plt.plot(vremya[:k], high[:k])
plt.title("Высокие частоты")
plt.subplot(3, 1, 3)
plt.plot(vremya[:k], middle[:k])
plt.title("Средние частоты")
plt.tight_layout()
plt.savefig("filters.png")

low = low / np.max(np.abs(low)) * 32767
high = high / np.max(np.abs(high)) * 32767
middle = middle / np.max(np.abs(middle)) * 32767

low = low.astype(np.int16)
high = high.astype(np.int16)
middle = middle.astype(np.int16)

f = wave.open("low.wav", "w")
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(chastota)
f.writeframes(low.tobytes())
f.close()

f = wave.open("high.wav", "w")
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(chastota)
f.writeframes(high.tobytes())
f.close()

f = wave.open("middle.wav", "w")
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(chastota)
f.writeframes(middle.tobytes())
f.close()

print("Готово")
