#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft, fftshift, fftfreq
from scipy.signal import hilbert, decimate, lfilter, butter


def main():
    fm_bandwidth = 34e3
    sampling_rate = 250e3
    bauds = 4160

    data = np.fromfile('noaa-12_256k.dat', dtype=np.complex64)
    # take the middle of the data (supposedly cleaner) 
    #data_portion = 1e-4
    #data = data[data.size * (1/2 - data_portion / 2) : data.size * (1/2 + data_portion / 2)]
    n = 2 * 2080 * sampling_rate/bauds
    data = data[data.size * 0.5 - n / 2:data.size*0.5 + n/2]
    
    # correct for a frequency shift: TODO: automate the detection of the shift
    f_error = -5e3 
    time_sampling = np.linspace(0, data.size / sampling_rate, data.size)
    shift = np.exp(2 * np.pi * 1j * f_error * time_sampling)
    data *= shift
    
    # filter to only keep the FM data
    signal_filtered = lowpass(data, fm_bandwidth, sampling_rate)
    show_signal(signal_filtered, title="FM signal")

    # compute the phase and the difference
    theta = np.angle(signal_filtered)
    delta_theta = np.angle(np.exp((theta[:-1] - theta[1:]) * 1j))

    # filter the AM signal to only keep component below 2.4khz
    demod_lp = lowpass(delta_theta, 2.4e3, sampling_rate)

    # demodulate the AM with an hilbert filter
    h = hilbert(demod_lp) 
    demodulated_signal = np.absolute(h)
    
    # phase align ? using sexy synchro info from the signal
    # did we correct for doppler? (try when we get an image)
    
    # decimate to get the real baud rate 
    dec = decimate(demod_lp, int(sampling_rate // bauds))
    show_signal(dec, title="Decimated and FM+AM demodulated", dot=True)

    # parse differents lines using the sync options
    # write image data to file
    # try to parse metadata
    
    print("There are %d samples at 4160 bauds" % (dec.size))

def lowpass(s, high, s_freq):
    b, a =  butter(5, high/s_freq, btype='lowpass')
    return lfilter(b, a, s)

def show_signal(s, title=None, dot=False):
    plt.subplot(2, 1, 1)
    plt.plot(np.linspace(-s.size, s.size, s.size), np.abs(fftshift(fft(s))))
    a = plt.gca()
    a.set_xlim([-s.size / 2, s.size / 2])

    if title:
        plt.title(title)

    plt.subplot(2, 1, 2)
    if dot:
        plt.plot(np.abs(s), 'o')
    else:
        plt.plot(np.abs(s))

    a = plt.gca()
    a.set_xlim([0, s.size])

    plt.show()

main()
