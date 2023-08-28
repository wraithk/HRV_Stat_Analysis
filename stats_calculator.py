import numpy as np 

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

def calculate_sampen(data_in, m=2, r=0.2):
    data = np.array(data_in)
    N = len(data)
    B = 0.0
    A = 0.0
    
    sd = np.std(data)
    threshold = r * sd
    
    def distance(v1, v2):
        rtn = 0
        for i in range(len(v1)):
            curr = abs(v1[i]-v2[i])
            if curr>rtn:
                rtn = curr
        return rtn
    
    def bmi(data, i): 
        counter = 0
        xmi = data[i:i+m]
        for j in range(0,N-m):
            if j == i:
                continue
            xmj = data[j:j+m]
            if distance(xmi,xmj) <= threshold:
                counter +=1
        rtn = counter/(N-m-1)
        return rtn

    def ami(data, i): 
        counter = 0
        xmi = data[i:i+m+1]
        for j in range(0,N-m):
            if j == i:
                continue
            xmj = data[j:j+m+1]
            if distance(xmi,xmj) <= threshold:
                counter +=1
        rtn = counter/(N-m-1)
        return rtn
    
    for i in range(0,N-m):
        B += bmi(data,i)
        A += ami(data,i)
    
    B = B/(N-m)
    A = A/(N-m)
    
    if A == 0 or B == 0: return np.inf
    
    rtn = -np.log(A/B)
    
    return rtn 

def calculate_d2(data):
    sd = np.std(data)
    N = len(data)

    r = 0.15*sd
    diff_count = 0
    for i in range(N):
        for j in range(i+1,N):
            if abs(data[i]-data[j]) < r:
                diff_count+=1  
    C = diff_count/(N*(N-1))
    return np.log(C)/np.log(r)

