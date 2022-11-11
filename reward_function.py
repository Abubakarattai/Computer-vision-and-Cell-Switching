# reward modelling for base station Energy optimization
import numpy as np
import pandas as pd

#Function for pathloss
def pathloss(l, b, d, x):
    pathloss = l + 10*b*np.log(d) + x
    return pathloss

# l is the reference pathloss at distance of 1m = 35.1dB
# b is pathloss exponent
# d is distance of user from BS
# x is the Guassian random variable

#equation 1 in overleaf document
# SNR function
def SNR(Pr,N):
    SNR = []
    for i in range(0,len(Pr)):
        S = Pr[i]/N
        SNR.apend(S)   
    return SNR
#print(SNR([100, 50, 40, 50], 100))
# Pr is the received power
# N is the white Guassian noise
# Each UE will have its own unique SNR value based on its location and the small cell it is connected to per time.

#equation 2 and 3 combined
# Function to determine the number of resource block (Nrb) required to satisfy user data rate requirement for each small cell
# Assume all users have the same minimum data rate requirement Q
# that means there is an array containing the SNR of all the users connected to the small cell per time.
def Nrb(Q,W,SNR):
    Nrb = []
    for i in range(0,len(SNR)):
        N = Q/(W*np.log2(1 + SNR[i]))
        Nrb.append(N)
    return Nrb
#print(Nrb(2000, 180, [0.9, 0.8, 0.3, 0.7]))
#print(Nrb(10, 180, 0.9))
# where Nrb is the number of resource blocks required by each user connect to a given small cell per time
# Q is the minimum data rate requirement of each user
# W is the bandwidth of one resource block i.e. 180Hz

#equation 4
# Cell load for each base station per time
# that means there is an array of Nrb for all the users connected to a base station per time
def load(Nrb, M):
    sum = 0
    for i in range(0,len(Nrb)):
        sum = sum + Nrb[i]
    load = sum/M
    return load
#print(load([2, 5, 7, 9 , 11], 100))
#M is the total number of resource blocks in the base station

#equation 6
# Function for total power consumption of all the small cells in the ultra dense network
# load is an array containing the load of all small cells in the Ultra-dense network per time

#FOR MACRO
Ntx_ma = 6
Pstatic_ma = 114.5
Delta_ma = 7.4
Pmax_ma = 26.5

# For small cell: we use pico cell
Ntx_pi = 2
Pstatic_pi = 2.3
Delta_pi = 4.6
Pmax_pi = 1
psleep_pi = 0.6   # different sleep mode values exist so we can have 0.2, 0.1 respectively

def Psum(Ntx,Pstatic,Delta,load,Pmax,Psleep):
    Psum = 0
    for i in range(0,len(load)):
        if load[i] == 0:
            Power = Psleep
        else:
            Power  = Ntx*(Pstatic + (Delta*load[i]*Pmax))
        Psum = Psum + Power
    return Psum
#print(Psum(130,4.7, [0,0.1], 20, 50))

#equation 9: This one is hard for me, we need to discuss more about this one
# Function for total Network through which is the sum of the throughput of all small cell in the ultra-dense network
# we calculate the total throughput of one small cell (TP) comprising the an array of the number of resource blocks and SNR 
# of all the users connected to the small cell per time
# then to get the total throughput of the network (TPsum), we sum the total throguput from all the small cells in the network
def TPsum(Nrb1, Nrb2, Nrb3, W, SNR1, SNR2, SNR3):
    TP1 = 0
    TP2 = 0
    TP3 = 0
    for i in range(0,len(Nrb1)):
        TP = Nrb1[i]*W*np.log2(1 + SNR1[i])
        TP1 = TP1 + TP
    
    for j in range(0,len(Nrb2)):
        TP = Nrb2[j]*W*np.log2(1 + SNR2[j])
        TP2 = TP2 + TP
        
    for k in range(0,len(Nrb3)):
        TP = Nrb3[k]*W*np.log2(1 + SNR3[k])
        TP3 = TP3 + TP
    TPsum = TP1 + TP2 + TP3
    return TPsum

#print(TPsum([1,3,5], [2,4,6], [3,5,7], 180, [0.3,0.8,0.9], [0.6, 0.5, 0.1], [0.7,0.2, 0.65]))
#  Nrb1, Nrb2, Nrb3 are seperate arrays containing the number of resource blocks of users connected to small cell 1, 2, 3 per time respectively
#  SNR1, SNR2, SNR3 are seperate arrays containing the number of the SNR values of users connected to small cell 1, 2, 3 per time respectively
#  W is the bandwidth of one resource block       

#equation 8
# Function for Total energy efficiency of the network
def Reward(TPsum,Psum):
    Reward = 0
    for i in range(0,len(Psum)):
        Reward = Reward + TPsum[i]/Psum[i]
        #Reward.append(EE) 
    return(Reward)


        
#print(EE([3,5,7],[1,3,5]))







