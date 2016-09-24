function filt = lowpass(cutoff, Fs)
%LOWPASS designs a 50-order FIR lowpass filter
%
% filt = lowpass(cutoff, Fs)
%
% cutoff        filter cutoff frequency (Hz)
% Fs            sampling frequency (Hz)

filt = fir1(50,cutoff/(Fs/2));