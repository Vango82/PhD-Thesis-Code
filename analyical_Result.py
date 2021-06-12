# Author: Vango
# Edit Time: 6/12/2021 8:52 AM
# Version: 1.0.0
# Analytical result of the blocking probability under different number of channels
import time

import matplotlib.pyplot as plt
import eB
import numpy as np
import time

start = time.time()
# assume the total offered load is 10 Erlang

lambda_1 = 4 * 0.3584  # arrival rate of priority level 1 traffic, which takes 40%
lambda_2 = 5 * 0.3584  # arrival rate of priority level 2 traffic, which takes 50%
lambda_3 = 1 * 0.3584  # arrival rate of priority level 3 traffic, which takes 10%
mu = 1  # define the service rate
A1 = lambda_1 / mu  # calculate the offer load of level 1 traffic
A2 = lambda_2 / mu  # calculate the offer load of level 2 traffic
A3 = lambda_3 / mu  # calculate the offer load of level 3 traffic

C = 15  # set the number of circuit (servers)

bp = np.zeros([C, 4])
# initialize the blocking probability matrix
# bp[:, 0] for the highest priority
# bp[:, 1] for the middle priority
# bp[:, 2] for the lowest priority
# bp[:, 3] for the average

for i in range(C):  # main loop
    bp[i, 0] = eB.erlangB(A1, i + 1)
    if bp[i, 0] >= 1:
        bp[i, 0] = 1
    bp[i, 1] = (eB.erlangB((A1 + A2), (i + 1)) * (A1 + A2) - bp[i, 0] * A1) / A2
    if bp[i, 1] >= 1:
        # print('B2 is greater than 1.')
        bp[i, 1] = 1
    bp[i, 2] = (eB.erlangB((A1 + A2 + A3), (i + 1)) * (A1 + A2 + A3) - bp[i, 0] * A1 - bp[i, 1] * A2) / A3
    if bp[i, 2] >= 1:
        # print('B3 is greater than 1.')
        bp[i, 2] = 1
    bp[i, 3] = np.mean(bp[i, 0:3])

end = time.time()
print("running time:",  end - start)  # show the running time

print(bp)  # output the results in console

fig1 = plt.figure(1)
x = np.linspace(1, C, C)  # define the horizontal axis
ax1 = fig1.add_subplot(1, 1, 1)
ax1.plot(x, bp[0:C, 0], '>-', label='Priority1')  # Priority 1
ax1.plot(x, bp[0:C, 1], 'o-', label='Priority2')  # Priority 2
ax1.plot(x, bp[0:C, 2], '*-', label='Priority3')  # Priority 3
ax1.plot(x, bp[0:C, 3], '--', label='Average')
ax1.set_xlim(1, C)
ax1.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
ax1.set_ylim(0, 1)
ax1.grid(True, which='major', axis='both')
ax1.legend(loc='best', numpoints=1)
plt.show()
