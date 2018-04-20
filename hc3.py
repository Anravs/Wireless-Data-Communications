__author__ = "Henry Choi"
__date__ = "3/19/2017"
# Henry Choi
# Wireless Data Communications
# Assignment 3
# March 24, 2017

import numpy as np
import matplotlib.pyplot as plt

g = np.array([[1, 0, 0],
              [1, 0, 1],
              [1, 1, 1]])

# # (output array, next state)
# trellis_graph = np.array([[([0,0,0],0), ([1,1,1],2)],
#                          [([0,1,1],0), ([1,0,0],2)],
#                          [([0,0,1],1), ([1,1,0],3)],
#                          [([0,1,0],1), ([1,0,1],3)]])

# homework test
# rb = np.array([[1,1,0,1,1,0,1,1,0,1,1,1,0,1,0,1,0,1,1,0,1]])

# (output array, next state)
trellis_graph = np.array([[[0,0,0], [0,1,1]],   # 0 - input was 0
                          [[0,0,1], [0,1,0]],   # 1 - input was 0
                          [[1,1,1], [1,0,0]],   # 2 - input was 1
                          [[1,1,0], [1,0,1]]])  # 3 - input was 1
trellis_prevstate = np.array([[0, 1],
                              [2, 3],
                              [0, 1],
                              [2, 3]])

def viterbi_enc(m):
    c = []
    for i in g:
        c.append(np.convolve(m, i) % 2)
    m_enc = np.array(c).T.flatten()
    return m_enc

def viterbi_dec(rb):
    decodeb = []
    for r in rb:  # iterate over all signal power values
        t_total = r.size//3
        msg = r.reshape(t_total, 3)  # break into chunks of 3 per message

        # forward propagation
        trellis = np.ones((t_total+1, 4, 2), dtype=np.int)
        trellis[:,:,0] *= 99999
        trellis[0,0,0] = 0  # first state is 0 weight.

        for t,word in enumerate(msg):
            for state in range(4):
                prevstate = trellis_prevstate[state]
                cum_weight = trellis[t][prevstate][:,0]  # cumulative weight for both prev states

                hamm_weight0 = ((word + trellis_graph[state][0]) % 2).sum() + cum_weight[0]
                hamm_weight1 = ((word + trellis_graph[state][1]) % 2).sum() + cum_weight[1]

                if hamm_weight0 < hamm_weight1:
                    trellis[t + 1][state][0] = hamm_weight0
                    trellis[t + 1][state][1] = prevstate[0]
                # elif hamm_weight0 > hamm_weight1:
                #     trellis[t + 1][state][0] = hamm_weight1
                #     trellis[t + 1][state][1] = prevstate[1]
                else:
                    trellis[t + 1][state][0] = hamm_weight1
                    trellis[t + 1][state][1] = prevstate[1]

        # back propagation
        backprop = trellis[1:, :, 1]  # trellis back prop indices, omit first layer

        traceback = [0]  # last state's trace back
        # iterate over backwards
        for i, s in enumerate(backprop[::-1]):
            traceback.append(s[traceback[-1]])
        tracefwd = traceback[-2::-1]  # omit first layer

        decode = []
        for s in tracefwd:
            decode.append(trellis_graph[s,0,0])  # g1 is just input bit, so can use that
        decode = np.array(decode)[:-2]  # cut off last two elements because of zero state reset
        decodeb.append(decode)

    return np.array(decodeb)


viterbi = True
b_num = 100
n = 100 # n is number of information bits

m = np.random.choice(2, n)  # m is message (1 x n) m_n binary
m_enc = viterbi_enc(m)  # encode from 4 to 7

b = np.logspace(-1, 1, b_num)[:,None]   # b is real value modulation scheme - column vector
yb = 2*(m_enc-0.5)*b                     # y is modulated signal
w = np.random.normal(0, 1, yb.shape[1])  # w is gaussian noise, u=0, var=1
zb = yb+w                                 # z is received signal at receiver
rb = (zb >= 0).astype('int')              # r is received symbols

m_hat = viterbi_dec(rb)        # m_hat is received symbols


e = np.abs(m_hat - m)           # e is bit error - (b x n)
esum = e.sum(axis=1)            # esum is number of errors for each b
P = esum/n                      # P is bit error rate probability

plt.figure()
plt.title('Bit Error Rate Probability vs. b (%s)' %
          ('With Viterbi' if viterbi else ''))
plt.ylabel('Probability / Variation')
plt.xlabel('b')
plot_prob, = plt.semilogx(b, P   , label='Probability')
plt.legend(handles=[plot_prob])
plt.ylim([-0.02, 0.5+0.02])
plt.xlim([.1, 10])  # zoom in