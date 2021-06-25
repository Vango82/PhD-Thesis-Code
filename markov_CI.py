# Author: Fan Li
# Edit Time: 6/16/2021 11:24 AM
# Version:1.0.0

import random
import time
import numpy as np
import matplotlib.pyplot as plt

start = time.time()  # set the starting time
# assume the total offered load is 10 Erlang
P = 3  # priority level is 3
C = 15  # number of channel (server)
MaxN = 100000  # total number of arrival
load = np.dot([4, 5, 1], 3.584 / 10)  # initialize the load vector
bp_mk = np.zeros([C, P+1])  # initialize the blocking probability vector

CI = 6  # set the loop count to get confidence intervals
b = np.zeros([CI, C, 4])  # 6 x 15 x 4 matrix, first dimension: CI, second dimension: channel, third dimension: priority
for z in range(CI):
    for c in range(C):
        arrival = np.zeros([P, 1])  # arrival counter of eac priority
        block = np.zeros([P, 1])  # blocking counter of each priority
        channel = np.zeros([c+1, 2])  # initialize the channel vector, occupy or not (first column), priority (second
        # column)
        Q = 0  # initialize the queue length
        for i in range(MaxN):
            rd_e = random.random()  # generate the random number to decide event (arrival/departure)
            if rd_e < np.sum(load) / (np.sum(load) + Q):  # event is an arrival
                rd_p = random.random()  # generate the random number to decide priority
                if rd_p < load[0] / np.sum(load):  # priority 1
                    priority = 1
                elif rd_p < (load[0] + load[1]) / np.sum(load):  # priority 2
                    priority = 2
                else:  # priority 3
                    priority = 3
                arrival[priority - 1] = arrival[priority - 1] + 1  # arrival counter increase
                search = np.where(channel[:, 0] == 0)  # find the free channel
                if search[0].size != 0:  # free channel exist
                    rnd_pk = np.random.randint(search[0].size)  # random select a channel
                    channel_no = search[0][rnd_pk]  # make sure the channel number
                    channel[channel_no, :] = [1, priority]  # update the channel information
                    Q = Q + 1  # increase queue length by 1
                else:  # no free channel exists
                    search = np.where(channel[:, 1] > priority)  # find the channel occupied by lower priority
                    if search[0].size == 0: # if there is no channel occupied by the lower priorities
                        block[priority - 1] = block[priority - 1] + 1  # blocking counter increase by 1
                    else:
                        rnd_pk = np.random.randint(search[0].size)  # randomly select a channel
                        channel_no = search[0][rnd_pk]  # find the channel number
                        get_priority = int(channel[channel_no, 1] - 1)  # get that priority
                        block[get_priority] = block[get_priority] + 1  # the blocking probability of that priority is
                        # increased by 1
                        channel[channel_no, :] = [1, priority]  # update the channel information
            else:  # event is a departure
                search = np.where(channel[:, 0] == 1)  # find the occupied channel
                channel_no = search[0][np.random.randint(search[0].size)]  # randomly select a channel
                channel[channel_no, :] = [0, 0]  # release the channel (update the channel information)
                Q = Q - 1  # decrease the queue length
        #  end of arrival loop
        bp_mk[c, 0] = block[0] / arrival[0]  # calculate the blocking probability of priority 1
        bp_mk[c, 1] = block[1] / arrival[1]  # calculate the blocking probability of priority 2
        bp_mk[c, 2] = block[2] / arrival[2]  # calculate the blocking probability of priority 3
        bp_mk[c, 3] = np.mean(bp_mk[c, 0:2])  # calculate the mean blocking probability of three priorities
    # end of circuit number loop
    b[z, :, :] = bp_mk
# end of confidence interval loop

b1 = np.zeros([1, C])  # initialize the blocking probability of priority 1 (average of CI times)
b2 = np.zeros([1, C])  # initialize the blocking probability of priority 2 (average of CI times)
b3 = np.zeros([1, C])  # initialize the blocking probability of priority 3 (average of CI times)
bt = np.zeros([1, C])  # initialize the blocking probability of average (average of CI times)

b1s = np.zeros([1, C])  # initialize the confidence interval of priority 1
b2s = np.zeros([1, C])  # initialize the confidence interval of priority 2
b3s = np.zeros([1, C])  # initialize the confidence interval of priority 3
bts = np.zeros([1, C])  # initialize the confidence interval of average

TINV = 2.57 / CI ** (1 / 2)  # calculate the parameter of

for i in range(C):  # derive the mean values (blocking probability & CI) of each priority
    b1[0, i] = np.mean(b[:, i, 0])  # priority 1
    # b1s[i] = np.std(b[:, i, 0]) * TINV
    b1s[0, i] = np.dot(np.std(b[:, i, 0]), TINV)  # confidence interval

    b2[0, i] = np.mean(b[:, i, 1])  # priority 2
    # b2s[i] = np.std(b[:, i, 1]) * TINV
    b2s[0, i] = np.dot(np.std(b[:, i, 1]), TINV)

    b3[0, i] = np.mean(b[:, i, 2])  # priority 3
    # b3s[i] = np.std(b[:, i, 2]) * TINV
    b3s[0, i] = np.dot(np.std(b[:, i, 2]), TINV)

    bt[0, i] = np.mean(b[:, i, 3])  # average
    # bts[i] = np.std(b[:, i, 3]) * TINV
    bts[0, i] = np.dot(np.std(b[:, i, 3]), TINV)
# end of confidence interval

end = time.time()  # get the ending time
print('Running time:', end - start, '\n')  # calculate the elapsed time

# plot the graph
x = np.linspace(1, C, C)  # set the range of x axis
plt.errorbar(x, b1[0], yerr=b1s[0], fmt='d-', ecolor='red', color='red', elinewidth=1, capsize=4, label='Priority1')  # draw the curve of priority 1
plt.errorbar(x, b2[0], yerr=b2s[0], fmt='o-', ecolor='green', color='green', elinewidth=1, capsize=4, label='Priority2')  # draw priority 2
plt.errorbar(x, b3[0], yerr=b3s[0], fmt='s-', ecolor='blue', color='blue', elinewidth=1, capsize=4, label='Priority3')  # draw priority 3
plt.errorbar(x, bt[0], yerr=bts[0], fmt='*-', ecolor='magenta', color='magenta', elinewidth=1, capsize=4, label='Average')  # draw the average
plt.xlim(1, C)  # set the range of x axis
plt.ylim(0, 1)  # set the range of y axis
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])  # set the ticks of X axis
plt.grid(True, which='major')
plt.grid(True, which='minor', axis='both')
plt.legend(loc='best', numpoints=1)  # set the legend
plt.title('Markov chain simulation result of bottleneck link\'s blocking probability')
plt.show()
