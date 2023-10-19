#!/usr/bin/env python

'''
Python functions for the Speech Coding (2016) laboratory measurement
Written by Tamas Gabor CSAPO <csapot@tmit.bme.hu>
Sep 27, 2016

LPC coding and decoding is based on audiolazy
https://pypi.python.org/pypi/audiolazy/0.04

Usage in jupyter notebook:
   from lp_functions import *
   % matplotlib inline
'''


import numpy as np
# import audiolazy as al
import matplotlib.pyplot as plt
import scipy.io.wavfile as io_wav
from scipy import signal
import peakutils
import IPython


# WAVREAD reads in waveform
#
# (x, Fs) = wavread(filename)
def wavread(filename):
    (Fs, x) = io_wav.read(filename)
    return (x, Fs)


# WAVWRITE writes out waveform
#
# wavwrite(y, Fs, filename)
def wavwrite(x, Fs, filename):
    scaled = np.int16(x / np.max(np.abs(x)) * 32767)
    io_wav.write(filename, Fs, scaled)


# RESAMPLE resamples signal
#
# x_new = resample(x, Fs_new, Fs_old)
def resample(x, Fs_new, Fs_old):
    # x_out = al.resample(x, Fs_old, Fs_new)
    # return x_out.take(al.inf)
    x_out = signal.resample(x, int(len(x) * Fs_new / Fs_old))
    return x_out


# CCLIP performs center clipping of signal 
#
#  y = cclip(x, minval, maxval)
#
#  Center clips the signal in x. 
#  Minval must be negative and maxval must be positive. 
#  Each elements of x is treated as follows: 
#  If x(i) > maxval, then y(i) = x(i) - maxval; 
#  If minval < x(i) < maxval, then y(i) = 0; 
#  If x(i) < minval, then y(i) = x(i) - minval; 
def cclip(x, minval, maxval):
    clipped = np.zeros(len(x))
    if maxval < 0 or minval > 0:
        raise Exception('Minimum value must be negative and maximum value must be positive')
    nx = len(x)
    zz = np.zeros(nx)
    oo = np.ones(nx)
    maxx = maxval * oo
    minn = minval * oo
    upper = np.maximum(x - maxx,zz)
    lower = np.minimum(x - minn,zz)
    clipped = upper + lower
    
    return clipped


# AUTOCORR calculates autocorrelation function
#
#  ac = autocorr(x)
def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[round(result.size / 2) : ]


# PITCH_DETECTOR Performs pitch detection on a speech waveform 
# 
#  pitch = pitch_detector(x, Fs)
#
#  x         speech data (vector)
#  Fs        sampling frequency in Hz (scalar)
#
#  pitch     pitch of frame in Hz or 0 if unvoiced (scalar)
def pitch_detector(x, Fs):
    # remove the dc value of the frame by subtracting the mean
    x -= np.mean(x)
    # find the minimum and maximum samples and center clip to 75% of those values
    x = cclip(x, 0.75 * np.min(x), 0.75 * max(x))
    # Compute the autocorrelation of the frame
    c = autocorr(x)
    # Find the maximum peak following Rx[0] # between 40 - 350 Hz
    c = c[25:]
    # peakind = signal.find_peaks_cwt(c, np.arange(25, 160)) 
    peakind = peakutils.indexes(c, thres = 0.5 / max(c), min_dist = 100)
    
    # Determine if the segment is unvoiced based on the 'voicing strength' 
    # (the ratio of the autocorrelation function at the peak pitch lag 
    # to the autocorrelation function lag=0)
    # If voicing strength is less than 0.25, call it unvoiced and set pitch = 0, 
    # otherwise compute the pitch from the % index of the peak
    # print(c[peakind[0]])
    if len(peakind) > 0 and c[peakind[0]] > 50000:
        pitch = Fs / (25 + peakind[0])
    else:
        pitch = 0
    
    return pitch


# IMPULSE_TRAIN generates an impulse train
# 
#  (pulses, next_delay) = impulse_train(T0, len, init_delay)
#
#  T0        period of the impulses in the impulse train (an integer value) 
#  len           length of impulse train in samples 
#  init_delay    delay of the first pulse (default 0) 
#
#  pulses        output pulse train 
#  next_delay    delay to first pulse in next frame 
def impulse_train(T0, length, init_delay = 0):
    pulses = np.zeros(length)
    next_delay = 0
    T0 = round(T0)
    
    # place impulses
    pulses[init_delay+1::T0] = 1
    max_pulse_time = 0
    for i in range(0, len(pulses)):
        if pulses[i] == 1:
            max_pulse_time = i
    if (sum(pulses) > 0):
        next_delay = max_pulse_time + T0 - length - 1
    else:
        next_delay = init_delay - length
    
    return (pulses, next_delay)


# WAVPLOT Plays speech and plots its waveform
# 
#  wavplot(x, Fs)
#
#  x         speech data
#  Fs        sampling frequency in Hz
def wavplot(x, Fs, ipython = True):
    # plot
    t = [i / Fs for i in range(0, len(x))]
    plt.plot(t, x)
    plt.xlabel('time [s]')
    plt.show()
    
    # playback
    if ipython:
        return IPython.display.Audio(x, rate=Fs)
    else:
        x_scaled = np.int16(x / np.max(np.abs(x)) * 32767)
        with al.AudioIO(True) as player: # True means "wait for all sounds to stop"
            player.play(x_scaled, rate=Fs)
            
    
# SOUNDSC Plays speech
#
# soundsc(x, Fs)
def soundsc(x, Fs):
    return IPython.display.Audio(x, rate=Fs)


# LPC Linear prediction coefficients
#
#  alpha = lpc(x, p)
#
#   finds the coefficients  A=[ 1 A(2) ... A(N+1) ],
#   of an Pth order forward linear predictor
#   Xp(n) = -A(2)*X(n-1) - A(3)*X(n-2) - ... - A(N+1)*X(n-P)
#   such that the sum of the squares of the errors
#   err(n) = X(n) - Xp(n)
def lpc(x, p = 12):
    alpha = al.lpc.autocor(x, p)
    return alpha


# FILTER filter signals
#
# y = filter(B, A, x)
#
#     Apply a 1-D digital filter to the data X.
#     'filter' returns the solution to the following linear,
#     time-invariant difference equation:
#
#           N                   M
#          SUM a(k+1) y(n-k) = SUM b(k+1) x(n-k)    for 1<=n<=length(x)
#          k=0                 k=0
#
#     where N=length(a)-1 and M=length(b)-1.
def filter(B, A, x):
    synth_filter = B / A
    y = np.array(list(synth_filter(x)))
    return y


# NORM calculates RMS (Root Mean Square)
#
# rms = norm(x)
def norm(x):
    rms = np.sqrt(np.mean(np.square(x)))
    return rms


# LOWPASS designs a lowpass filter
#
# filt = lowpass(cutoff, Fs)
#
# cutoff        filter cutoff frequency (Hz)
# Fs            sampling frequency (Hz)
def lowpass(cutoff, Fs):
    filt = al.lowpass.pole(cutoff / Fs)
    return filt


# MEDFILT1 median filter
#
# out = medfilt1(x, n)
def medfilt1(x, n = 3):
    return signal.medfilt(x, n)


# RANDN random numbers, list of frlen values
#
# randomlist = randn(length)
def randn(frlen):
    return np.random.randn(frlen)
