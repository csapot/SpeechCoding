function [pitch] = pitch_detector(x, Fs) 
%PITCH_DETECTOR Performs pitch detection on a speech waveform 
% 
% pitch = pitch_detector(x, Fs)
%
% x         speech data (vector)
% Fs        sampling frequency in Hz (scalar)
% pitch     pitch of frame in Hz or 0 if unvoiced (scalar)

% First, remove the dc value of the frame by subtracting the mean
x = x-mean(x); 

% Then find the minimum and maximum samples and center clip to 
% 75% of those values
x = cclip(x,0.75*min(x),0.75*max(x));

% Compute the autocorrelation of the frame
c = xcorr(x,'coeff');
zero_ind = find(c==max(c));
c = c(zero_ind:length(c));

% Find the maximum peak following Rx[0]
[peakval peakind] = peak(c);

% Determine if the segment is unvoiced based on the 'voicing strength' 
% (the ratio of the autocorrelation function at the peak pitch lag 
% to the autocorrelation function lag=0)
% If voicing strength is less than 0.25, call it unvoiced and set pitch = 0, 
% otherwise compute the pitch from the % index of the peak
if peakval > .25
    t0 = peakind/Fs;
    pitch = 1/t0;
else
    pitch = 0;
end