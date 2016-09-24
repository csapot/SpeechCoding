function [peakval,peakindex] = peak(x) 
%PEAK Detects value and index of peak in autocorrelation function. 
% [peakval peakindex] = peak(x) locates the value and index of the 
% largest peak in the vector x other than Rx[0]. x must be an 
% autocorrelation function with maximum value Rx[0] its first element. 
% 
if ( (size(x,1) > 1) & (size(x,2) > 1) ) 
    error ('Signal must be a vector') 
end
x = x(:); 
if ( x(1,1) ~= max(x) ) 
    error('Input must be an autocorrelation function with Rx[0] as first element')
end
nx = length(x); 
flag = 0; 
i = 1; 
while (flag == 0) 
    if ( x(i,1) < 0 ) 
        flag = 1; 
    else
        i = i+1; 
    end
end
[peakval peakindex] = max(x(i:nx)); 
peakindex = peakindex+i-1;