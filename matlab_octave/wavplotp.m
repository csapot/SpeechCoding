function wavplotp(wav,pitch,Fs)
%WAVPLOTP Plays speech and plots its waveform with the pitch contour
%overlaid
%
% wavplotp(wav,pitch,Fs)
% 
% wav       speech data
% pitch     vector of pitch values
% Fs        sampling frequency in Hz

time=1:length(wav);
time=time/Fs;
time_p=1:length(pitch);
frlen=length(wav)/length(pitch);
time_p=time_p*frlen/Fs;
figure;
plotyy(time,wav,time_p,pitch);
xlabel('time [s]');
soundsc(wav,Fs);