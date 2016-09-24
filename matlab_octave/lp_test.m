function lp_test(wavfile_in, wavfile_out, p) 
%LP_TEST Analyzes and synthesized speech waveform
% 
% lp_test(wav_in, wav_out, p)

Fs8 = 8000;
[x, Fs] = wavread(wavfile_in);
pkg load signal
x8 = resample(x, Fs8, Fs);
[coeff, gain, pitch] = lp_coder(x8, p, Fs8);
% pitch(pitch > 0) = 0;
x8_out = lp_decoder(coeff, gain, pitch, Fs8);
wavwrite(x8_out, Fs8, wavfile_out);