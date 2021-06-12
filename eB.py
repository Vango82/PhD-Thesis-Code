# Author: Vango
# Edit Time: 6/11/2021 11:25 AM

import numpy as np
import math


def erlangB(A, k):  # 'A' is the total offered traffic (Erlang), k is the number of circuit

    if A <= 0:  # if offered load is less than or equal to zero, then blocking probability is zero
        return 0

    k = math.floor(k)  # round the 'k' value to nearest integer
    if k <= 0:  # 'k' value is less than or equal to zero, no circuit can be used
        block = 1  # the blocking probability equal to 1
        return block
    else:  # there is at least one circuit can be used
        b = np.ones(k)  # initialize the 'b' array to store the blocking probability
        for i in range(k):  # the main loop
            if i == 0:  # there is one circuit, note that the index begins from 0
                b[i] = A / (1 + A)
            else:  # calculate the blocking probability based on the last calculation
                b[i] = (A * b[i - 1]) / ((i + 1) + A * b[i - 1])
        block = b[i]  # return the last value of 'b' array
    return block


# test1:
# print(erlangB(-20, -100))

# test2:
# print(erlangB(0, 1))

# test3:
# print(erlangB(1, 0))

# test4:
# print(erlangB(1, 1))

# test5:
# print(erlangB(3000, 3000))
