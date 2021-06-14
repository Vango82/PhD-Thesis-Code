clear all;

tic;

C = 15;

lambda_1 = 4 * 0.3584; %arrival rate of priority level 1 traffic
lambda_2 = 5 * 0.3584; %arrival rate of priority level 2 traffic
lambda_3 = 1 * 0.3584; %arrival rate of priority level 3 traffic

mu = 1; %initialize the service rate

A1 = lambda_1 / mu; %calculate the offer load of level 1 traffic
A2 = lambda_2 / mu; %calculate the offer load of level 2 traffic
A3 = lambda_3 / mu; %calculate the offer load of level 3 traffic

%C=10; %initialize the number of circuit (server)

bp = zeros(C, 4);

for i = 1 : C
    
    bp(i, 1) = ErlangB(A1, i);
    if bp(i, 1) >= 1
        bp(i, 1) = 1;
    end
    
    bp(i, 2) = (ErlangB(A1+A2,i)*(A1+A2)-bp(i,1)*A1)/A2;
    if bp(i,2) >= 1
        disp('B2 is greater than 1');
        bp(i, 2) = 1;
    end
    
    bp(i, 3) = (ErlangB(A1+A2+A3,i)*(A1+A2+A3)-bp(i,1)*A1-bp(i,2)*A2)/A3;
    if bp(i,3) >= 1
        disp('B3 is greater than 1');
        bp(i, 3) = 1;
    end
 
    bp(i, 4) = mean(bp(i, 1:3));
    
end

%plot graph
i = 1 : C;
plot(i, bp(i, 1), ':d');
hold on;
plot(i, bp(i, 2), ':o');
hold on;
plot(i, bp(i, 3), ':*');
hold on;
plot(i, bp(i, 4), ':s');

xlim([1, C]);
ylim([0, 1]);
%set(gca, 'YTick', 0:0.1:1);
%set(gca, 'yticklabel',{'0%', '5%', '10%', '15%' ,'20%', '25%', '30%', '35%', '40%'});
set(gca, 'XTick', 1:1:C);                           

%title('Blocking probability of bottleneck link analytical result');
title('Analytical result of bottleneck link''s blocking probability');
xlabel('Number of channel');
ylabel('Blocking probability');
legend('Priority 1', 'Priority 2', 'Priority 3', 'Average');

grid on;

%write to the file
fid = fopen('Single node analytical.txt', 'w');
% fprintf(fid, '[Priority1 Priority2 Prirotiy3 Average   ]');
% fprintf(fid,'%c\r\n', ' '); 

for row = 1 : C
    fprintf(fid, '%d', row);
    for column = 1 : 4
        fprintf(fid, '%c', ' & ');
        fprintf(fid, '%9.7f', bp(row, column));
    end
    fprintf(fid,'%c', ' \\ \hline');
    fprintf(fid, '\r\n'); 
end

% for row=1:C
%     %fprintf(fid, '%c', '[');
%     for column=1:4
%         fprintf(fid, '%9.7f ', bp(row, column));
%     end
%     %fprintf(fid,'%c', '];');
%     fprintf(fid, '\r\n'); 
% end

fclose(fid);

dlmwrite('ana.dat', bp);

toc;