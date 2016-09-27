#!/usr/bin/env python

'''
Python functions for the Speech Coding (2016) laboratory measurement
Written by Tamas Gabor CSAPO <csapot@tmit.bme.hu>
Sep 27, 2016

Usage in jupyter notebook:
   from lp_codec_draft import *
   (coeff, gain, pitch) = lp_coder(x, p, Fs)
   y = lp_decoder(coeff, gain, pitch, Fs)
'''

from lp_functions import *


#########################
# YOUR TASKS START HERE #
#########################

# LP_CODER Analyzes speech waveform into pitch, gain, coefficients 
#  
# (coeff, gain, pitch) = lp_coder(x, p, Fs)
# 
#  x         input signal 
#  p         order of LPC model 
#  Fs        sampling frequency (Hz)
#  
#  coeff     list of LP coefficients (one per frame)
#  gain      list of gain values (one per frame) 
#  pitch     list of pitch values (one per frame), 0=unvoiced 
def lp_coder(x, p, Fs = 8000):
    # length of speech frames (30 ms) in samples
    frlen = round(0.03 * Fs)
    # output vector length = number of frames
    nframes = al.ceil(len(x) / frlen)
    # memory is allocated in advance - for speed
    coeff = [type('', (), {})() for c in range(nframes)] # list of empty types
    gain = np.zeros(nframes) # list of zeros
    pitch = np.zeros(nframes) # list of zeros
    
    # YOUR TASK
    # Design a lowpass filter with the 'lowpass' function! (but do not apply it yet)
    # the cutoff frequency should be 500 Hz, because we are interested
    # in the fundamental frequency, which is 80-320 Hz for adults
    # . . .
    
    
    # every iteration of the loop will process one speech frame
    for i in range(nframes):
        # we take the next frame from the input signal
        frame = x[int(i * frlen) : int((i + 1) * frlen)]
        
        # YOUR TASK
        # Calculate the LPC coefficients of the frame ('lpc' function) and 
        # store them in the coefficient matrix
        # . . .
        
        
        # YOUR TASK
        # Calculate the LPC residual signal and its energy ('norm' function)
        # write the result into the gain vector
        # . . .
        
        
        # YOUR TASK
        # Determine whether the current frame is voiced, and estimate the 
        # fundamental frequency. First, apply the 500 Hz lowpass filter, 
        # and after that use the 'pitch_detector' function
        # . . .
        
        
    # YOUR TASK
    # Remove the clearly erroneous values from the pitch vector using
    # median filtering, help(medfilt1)
    # . . .
    
    
    # output
    return (coeff, gain, pitch)



#########################
# YOUR TASKS START HERE #
#########################

# LP_DECODER Synthesize speech waveform from LPC coefficients, gain and pitch 
#  
# y = lp_decoder(coeff, gain, pitch, Fs) 
#
# coeff     list of LP coefficients (one per frame)
# gain      list of gain values (one per frame) 
# pitch     list of pitch values (one per frame), 0=unvoiced 
# Fs        sampling frequency (Hz) 
# 
# y         synthesized speech signal 
def lp_decoder(coeff, gain, pitch, Fs = 8000):
    # error handling / test the length of parameters
    if len(coeff) != len(gain) or len(coeff) != len(pitch):
        raise Exception('length of lists not consistent')
    
    # length of speech frames (30 ms) in samples
    frlen = round(0.03 * Fs)
    # number of frames
    nframes = len(coeff)
    # memory is allocated in advance for the output - for speed
    y = np.zeros(nframes * frlen)
    # delay of the impulse sequence
    delay = 0
    prev = np.zeros(frlen)
    
    # loop for all frames
    for i in range(nframes):
        # the pitch value stores whether the frame is voiced or unvoiced
        if pitch[i] > 0:
            # YOUR TASK
            # Create the voiced source signal. For this, first
            # calculate the length of the fundamental period and create
            # an impulse sequence ('impulse_train' function) for the frame
            # (also, save the new delay as it will be necessary for the next frame)
            # . . .
            
            
        else:
            # YOUR TASK
            # Create the unvoiced source signal (using the 'randn' function)
            # . . .
            
            
        
        # YOUR TASK
        # Now apply the LPC filter for the source signal ('filter' function)
        # . . .
        
        
        # YOUR TASK
        # Normalize the speech signal in order that its energy will be 1
        # (do not divide by zero!)
        # . . .
        
        
        # restore filter state across frames
        # without this there would be breaks across consecutive frames
        # as a result of improper filtering at the end of the frame
        if pitch[i] > 0:
            frame[0:len(prev)] = prev[0:len(prev)]
            prev = frame[-int(round(Fs / pitch[i])):].copy()
        else:
            prev = frame[-int(round(Fs / 200)):].copy()
        
        # YOUR TASK
        # Set the energy of the frame (multiply it with the gain value)
        # . . .
        
        
        # YOUR TASK
        # Place the frame to the output signal
        # . . .
        y[int(i * frlen) : int((i + 1) * frlen)] = 
        
        
    # normalize amplitude
    y /= max(y)
    return y
