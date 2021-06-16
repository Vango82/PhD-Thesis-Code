tic;
clear all;

P = 3; %priority level is 3
C = 15; %number of channel (server)

load = [4, 5, 1].*3.584/10; %offer load vector
MaxN = 1e5; %total number of arrival
bp_mk = zeros(C, P); %initialize the output result vector

CI = 6; %set the loop count to get the Confidence Interval
b = zeros(CI, C, 4); %initialize the vector to store the blocking probability

for z = 1 : CI %loop for the CI
    for C = 1 : C %loop from 1 to C circuits
        arrival = zeros(1,P); %initialize the arrival vector
        block = zeros(1,P); %initialize the block vector
        channel = zeros(C,2); %initialize the channel vector, 1-occupy or not; 2-priority
        Q = 0; %initialize the queue length

        for i=1 : MaxN %for all simulation

            rd = rand(); %generate a random number

            if rd < sum(load)/(sum(load)+Q) %event is an arrival

                rd = rand(); %generate a random number
                if rd < load(1)/sum(load)
                    priority = 1;
                elseif rd < (load(1)+load(2))/sum(load)
                    priority = 2;
                else
                    priority = 3;
                end

                arrival(priority) = arrival(priority)+1; %increase 'arrival(priority)' vector
                slots = find(channel(:, 1)==0); %find all the empty slots
                if ~isempty(slots) %if exist
                    channel_no = slots(randi(length(slots),1)); %random select a channel
                    channel(channel_no, :) = [1, priority]; %record the channel status
                    Q = Q + 1; %queue length increase 1
                else
                    slots = find(channel(:, 2)>priority); %find all the slots whose priority is less than current priority
                    if isempty(slots) %if there is no such slots
                        block(priority) = block(priority)+1; %current request is blocked
                    else
                        channel_no = slots(randi(length(slots), 1));  %random select a channel
                        block(channel(channel_no, 2)) = block(channel(channel_no, 2))+1; %kick that burst being transmitted
                        channel(channel_no, :) = [1, priority]; %assing the request
                    end
                end

            else %event is a depature
                slots = find(channel(:, 1)==1); %find all the occupied channels
                channel_no = slots(randi(length(slots), 1)); %random select a channel
                channel(channel_no, :) = [0, 0]; %release that channel
                Q = Q - 1; %queue length decrease 1
            end
        end

        bp_mk(C, 1) = block(1)/arrival(1); %calculate the blocking of priority 1
        bp_mk(C, 2) = block(2)/arrival(2); %calculate the blocking of priority 2
        bp_mk(C, 3) = block(3)/arrival(3); %calculate the blocking of priority 3
        bp_mk(C, 4) = mean(bp_mk(C, 1:3)) %calculate the average blocking
    end
    b(z, :, :) = bp_mk;     
end

b1=zeros(C, 1);
b2=zeros(C, 1);
b3=zeros(C, 1);
bt=zeros(C, 1);

b1s=zeros(C, 1);
b2s=zeros(C, 1);
b3s=zeros(C, 1);
bts=zeros(C, 1);

TINV = 2.57/sqrt(CI); %derive the parameter of CI

for i = 1:C
    b1(i) = mean(b(:, i, 1)); %calculat the mean value of blocking proabablity
    b1s(i) = std(b(:, i, 1)) * TINV; %calculate the error bar for CI
    
    b2(i) = mean(b(:, i, 2));
    b2s(i) = std(b(:, i, 2)) * TINV;
    
    b3(i) = mean(b(:, i, 3));
    b3s(i) = std(b(:, i, 3)) * TINV;
    
    bt(i) = mean(b(:, i, 4));
    bts(i) = std(b(:, i, 4)) * TINV;
end

%plot the graph
i = 1 : C;
errorbar(i, b1(i), b1s(i), '-.d');
hold on;
errorbar(i, b2(i), b2s(i), '-.o');
hold on;
errorbar(i, b3(i), b3s(i), '-.*');
hold on;
errorbar(i, bt(i), bts(i), '-.s');

xlim([1, C]);
ylim([0, 1]);
set(gca, 'YTick', (0:0.05:1));
set(gca, 'XTick', (1:1:C));  

title('Markov chain simulation result of bottleneck link''s blocking probability');
xlabel('Number of channel');
ylabel('Blocking probability');
legend('Priority 1', 'Priority 2', 'Priority 3', 'Average');
grid on;
% 
% 
% fid = fopen('Markov.txt', 'w');
% 
% for row = 1 : C
%     fprintf(fid, '%d', row);
%     for column = 1 : 4
%         fprintf(fid, '%c', ' & ');
%         fprintf(fid, '%9.7f', bp_mk(row, column));
%     end
%     fprintf(fid,'%c', ' \\ \hline');
%     fprintf(fid, '\r\n'); 
% end
% 
% dlmwrite('mak.dat', bp_mk);

toc;