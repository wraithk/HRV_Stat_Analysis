import numpy as np 
import scipy.spatial

def calculate_rmssd(data):
    diffs = np.diff(data)
    diff_squared = np.square(diffs)
    mean_diff_squared = np.mean(diff_squared)
    rmssd = np.sqrt(mean_diff_squared)
    return rmssd

def calculate_rmse(data):
    average = np.mean(data)
    error = data-average 
    diffs_squared = np.square(error)
    mean_diff_squared = np.mean(diffs_squared)
    rmse = np.sqrt(mean_diff_squared)
    return rmse

def mean_interval(data):
    return np.mean(data)

def calculate_sampen(data, m=2, r=0.2):
    N = len(data)
    A_counter = 0
    B_counter = 0.0
    std = np.std(data)
    threshold = r * std

    def distance(v1, v2):
        rtn = 0
        for i in range(len(v1)):
            curr = abs(v1[i]-v2[i])
            if curr>rtn:
                rtn = curr
        return rtn
    #Calculate sum for A 
    for i in range(N-m):
        curr_A_counter = 0
        group_1 = data[i:i+m+1]
        for j in range(i+1,N-m):
            curr_group_2 = data[j:j+m+1]
            if distance(group_1,curr_group_2) <= threshold:
                curr_A_counter += 1
        A_counter += curr_A_counter / (N-m-1)
    #Calculate sum for B
    for i in range(N-m+1):
        curr_B_counter = 0
        group_1 = data[i:i+m]
        for j in range(i+1,N-m+1):
            curr_group_2 = data[j:j+m]
            if distance(group_1,curr_group_2) <= threshold:
                curr_B_counter += 1
        B_counter += curr_B_counter / (N-m)
    A = A_counter/(N-m-1)
    B = B_counter/(N-m)
    
    return -np.log(A/B)

def calculate_d2(data,r=0.15):
    N = len(data)
    std = np.std(data)
    threshold = r*std
    C_counter = 0
    for i in range(N):
        for j in range(i+1,N):
            if abs(data[i]-data[j])<=threshold:
                C_counter += 1
    C = C_counter/(N*(N-1))
    return np.log(C)/np.log(r)

