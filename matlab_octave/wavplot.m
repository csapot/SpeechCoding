function wavplot(wav,Fs)
%WAVPLOT Plays speech and plots its waveform
% 
% wavplot(wav,Fs)
%
% wav       speech data
% Fs        sampling frequency in Hz

time=1:length(wav);
time=time/Fs;
figure;
plot(time,wav);
xlabel('time [s]');
soundsc(wav,Fs);