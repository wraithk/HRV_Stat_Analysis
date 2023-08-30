import numpy as np
import random
from scipy.spatial.distance import pdist, squareform
import stats_calculator as s

def main():
    test_intervals = np.genfromtxt('test_intervals.txt', delimiter='\t')
    test_intervals = test_intervals * 1000
    test_rmssd = s.calculate_rmssd(test_intervals)
    print(f"test RMSSD: {test_rmssd}")

    test_sampen = s.calculate_sampen(test_intervals)
    print(f"test SampEn: {test_sampen}")

    test_d2 = s.calculate_d2(test_intervals)
    print(f"test D2: {test_d2}")


# Calculates RRIs from the R Peaks data
def calculate_r_r_intervals(data):
    times = data[:,0]
    r_r_intervals = np.diff(times).astype(float) * 1000.00
    return r_r_intervals

if __name__ == '__main__':
    main()