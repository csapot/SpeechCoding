function [p, next_delay] = impulse_train(period ,len, init_delay) 
%IMPULSE_TRAIN generates an impulse train
% 
% [p, next_delay] = impulse_train(period ,len, init_delay)
%
% period        period of the impulses in the impulse train (an integer or real value). 
% len           length of impulse train in samples 
% init_delay    delay of the first pulse (default 0) 
%
% p             output pulse train 
% next_delay    delay to first pulse in next frame 


if nargin < 3, 
    init_delay = 0; 
end
% convert period to integer
period = round(period);
% Initialize impulse train. 
p = zeros(1,len); 
% Place impulses 
pulse_times = init_delay+1:period:len; 
if ~isempty(pulse_times), 
    p(pulse_times) = ones(size(pulse_times)); 
    % find time to next pulse 
    next_delay=max(pulse_times)+period-len-1; 
else
    next_delay = init_delay - len; 
end