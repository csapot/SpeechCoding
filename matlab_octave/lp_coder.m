function [coeff, gain, pitch] = lp_coder(x, p, Fs) 
%LP_CODER Analyzes speech waveform into pitch, gain, coefficients 
% 
% [coeff, gain, pitch] = lp_coder(x, p)
%
% x         input signal 
% p         order of LPC model 
% Fs        sampling frequency (Hz)
% 
% coeff     matrix of LP coefficients 
%           (column index = frame number; 
%           row index = coefficient number) 
% gain      vector of gain values (one per frame) 
% pitch     vector of pitch values (one per frame), 0=unvoiced 

% x should be a column vector - just for sure
x = x(:);
% length of the speech frame (30 ms) in samples
frlen = round(0.03 * Fs);
% length of the input vector
s = size(x);
% length of the output vector = number of frames
len = floor(s(1) / frlen);
% memory is allocated in advance - for speed
gain = zeros(1, len); 
pitch = zeros(1, len); 
coeff = zeros(p+1, len); 
coeff(1,:) = ones(1,len); 

% YOUR TASK
% Design a lowpass filter with the 'lowpass' function! (but do not apply it yet)
% the cutoff frequency should be 500 Hz, because we are interested
% in the fundamental frequency, which is 80-320 Hz for adults
% . . .


% every iteration of the loop will process one speech frame
for i = 1:len 
    % we take the next frame from the input signal
    frame = x(((i-1)*frlen+1):(i*frlen));
    
    % YOUR TASK
    % Calculate the LPC coefficients of the frame ('lpc' function) and 
    % store them in the coefficient matrix
    % help: the i-th column of the coeff matrix: coeff(:, i)
    % . . .
    
    
    % YOUR TASK
    % Calculate the LPC residual signal and its energy ('norm' function)
    % write the result into the gain vector
    % . . .
    
    
    % YOUR TASK
    % Determine whether the current frame is voiced, and estimate the 
    % fundamental frequency. First, apply the 500 Hz lowpass filter, 
    % and after that use the 'pitch_detector' function
    % . . .
    
    
end
% end of loop

% YOUR TASK
% Remove the clearly erroneous values from the pitch vector using
% median filtering
% . . .



