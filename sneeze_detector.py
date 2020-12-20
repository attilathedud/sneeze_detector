#!/usr/bin/env python3
""" Sneeze/loud sound detector """
import math
import numpy as np

try:
    import sounddevice as sd
    import soundfile as sf

    sound_threshold = 5
    previous_sounds_to_hold = 10

    previous_sounds = []
    
    def reset_previous_sounds():
       previous_sounds.clear()
       for i in range(previous_sounds_to_hold):
           previous_sounds.append(0)

    reset_previous_sounds()

    data, fs = sf.read('blessyou.wav', dtype='float32') 

    samplerate = sd.query_devices(None, 'input')['default_samplerate']
    delta_f = 24
    fftsize = math.ceil(samplerate / delta_f)

    def callback(indata, frames, time, status):
        if any(indata):
            magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
            magnitude *= 10000 / fftsize

            previous_sounds.pop(0)
            previous_sounds.append(np.average(magnitude))

            if(np.average(previous_sounds) > sound_threshold):
                reset_previous_sounds()
                sd.play(data, fs) 
                sd.wait()
    
    with sd.InputStream(channels=1, callback=callback,
                        blocksize=int(samplerate * 50 / 1000)): 
        while True:
            response = input() 
except KeyboardInterrupt:
    print("Cancelled by user")
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))
