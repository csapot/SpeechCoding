function clipped = cclip(x,minval,maxval) 
%CCLIP performs center clipping of signal 
% y = cclip(x,minval,maxval) center clips the signal in x. 
% Minval must be negative and maxval must be positive. 
% Each elements of x is treated as follows: 
% If x(i) > maxval, then y(i) = x(i) - maxval; 
% If minval < x(i) < maxval, then y(i) = 0; 
% If x(i) < minval, then y(i) = x(i) - minval; 
% 
if ( (size(x,1) > 1) & (size(x,2) > 1) ) 
    error ('Signal must be a vector') 
end
if ( (length(maxval) > 1) | (length(minval) > 1) ) 
    error ('Minimum and maximum values must be scalars') 
end
if ( (maxval < 0) | (minval > 0) ) 
    error ('Minimum value must be negative and maximum value must be positive') 
end
x = x(:); 
nx = length(x); 
zz = zeros(nx,1); 
oo = ones(nx,1); 
maxx = maxval * oo; 
minn = minval * oo; 
upper = max(x-maxx,zz); 
lower = min(x-minn,zz); 
clipped = upper + lower;