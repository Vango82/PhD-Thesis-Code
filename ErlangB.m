function [block] = ErlangB(A, k)
%ErlangB, function by Fan Li
%[block] = Erlang(A,K) returns the blocking probability of 
%a telecommunication system with A offered load and k circuits (servers).

k=floor(k);
b=ones(1,k);

for i=1:1:k
    if i==1
        b(i)=A/(1+A);
    else
        b(i)=(A*b(i-1))/(i+A*b(i-1));
    end
end

if k<=0 %if there is no circuit/server
    block=1; 
else
    block=b(k);
end

end

