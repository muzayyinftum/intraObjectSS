import importlib

from numpy import average, median
methods = importlib.import_module("2-METHOD")

rate, sample = methods.sampling_audio('stegoaudioDataset/Audio/data1_mono.wav')

difference = []
for i in range(len(sample) - 1):
    difference.append(abs(sample[i] - sample[i + 1]))

print(max(difference), min(difference), average(difference), median(difference))