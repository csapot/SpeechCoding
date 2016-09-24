function y = lp_decoder(coeff, gain, pitch, Fs) 
%LP_DECODER Synthesize speech from pitch, gain, and coefficients 
% 
% y = lp_decoder(coeff, gain, pitch, Fs) 
%
% coeff     matrix of LP coefficients 
%           (column index = frame number; 
%           row index = coefficient number) 
% gain      vector of gain values (one per frame) 
% pitch     vector of pitch values (one per frame), 0=unvoiced 
% Fs        sampling frequency (Hz) 
% 
% y         synthesized speech signal 


% error handling 
if (nargin < 3), 
    error('There must be 3 or 4 input arguments'); 
end; 
[nrows nframes]=size(coeff); 
if (nframes ~= length(pitch)), 
    error('Pitch vector has illegal length'); 
end; 
if (nframes ~= length(gain)), 
    error('Gain vector has illegal length'); 
end; 

% frame length 
frlen = round(0.03*Fs); 
% memory is allocated in advance for the output - for speed
y = zeros(nframes*frlen,1); 
% variables for the delay of the impulse sequence and 
% for the LPC filter state
delay = 0; 
filt_state = zeros(size(coeff,1)-1,1); 

% loop for all frames
for i=1:nframes
    % the pitch value stores whether the frame is voiced or unvoiced
    if pitch(i) > 0 
        % YOUR TASK
        % Create the voiced source signal. For this, first
        % calculate the length of the fundamental period and create
        % an impulse sequence ('impulse_train' function) for the frame
        % (also, save the new delay as it will be necessary for the next frame)
        % . . .
        
    else
        % YOUR TASK
        % Create the unvoiced source signal (using the 'randn' function)
        % . . .
        
        
    end
    
    % YOUR TASK
    % Normalize the source signal in order that its energy will be 1
    % (do not divide by zero!)
    % . . .
    
    
    % YOUR TASK
    % Now apply the LPC filter for the source signal ('filter' function)
    % In order to avoid breaks in the reconstructed speech,
    % save the state of the filter to the 'filt_state' variable
    % . . .
    
    
    % YOUR TASK
    % Set the energy of the frame (multiply it with the gain value)
    % . . .
    
    
    % YOUR TASK
    % Place the frame to the output signal
    % . . .
    y((i-1)*frlen+1:i*frlen) = 
end

% normalize
y = y / max(y);