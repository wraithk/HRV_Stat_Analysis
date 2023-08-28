import numpy as np
import os
import random
from scipy.spatial.distance import pdist, squareform
import stats_calculator as s

def main():
    #The directory where this file lives
    ROOTDIR = os.path.dirname(__file__)
    RR_INTERVAL_DATA_COL = 1

    output = np.empty((0,5))
    #Import baseline and conditions R Peaks data
    #These files are in "<timestamp>\t<rr_interval>" format (tab separated).
    #We don't need the timestamp so strip it out.
    input_baseline_data = np.genfromtxt(os.path.join(ROOTDIR, 'Data', 'P5 D1 Baseline HR_R-Peaks_0.1-5.1.txt'), delimiter='\t', usecols=(RR_INTERVAL_DATA_COL))
    input_condition_data = np.genfromtxt(os.path.join(ROOTDIR, 'Data','P5 D1 Drive HR_R-Peaks_16.49-21.49.txt'), delimiter='\t', usecols=(RR_INTERVAL_DATA_COL))

    #Calculate the baseline RRIs
    baseline_intervals = input_baseline_data
    #Calculate the HRV measures of the baseline 
    baseline_rmssd = s.calculate_rmssd(baseline_intervals)
    baseline_rmse = s.calculate_rmse(baseline_intervals)
    baseline_mean = s.mean_interval(baseline_intervals)
    baseline_sampen = s.calculate_sampen(baseline_intervals)

    #D2 is not being output in the txt, its validity is still being checked
    baseline_d2 = s.calculate_d2(baseline_intervals)
    print("Baseline D2:", baseline_d2)

    #Calculate the original condition RRIs
    original_condition_intervals = input_condition_data
    #Calculate the original condition HRV measures
    original_condition_rmssd = s.calculate_rmssd(original_condition_intervals)
    original_conditon_rmse = s.calculate_rmse(original_condition_intervals)
    original_condition_mean = s.mean_interval(original_condition_intervals)
    original_condition_sampen = s.calculate_sampen(original_condition_intervals)

    #Remove R-R intervals at random and recalculate chosen measures
    for counter in range(1000):
        print(counter)
        deleted_intervals, num_deleted = rand_delete(original_condition_intervals,0.1)
        new_row = calculate_and_write(deleted_intervals,num_deleted)
        output = np.vstack((output,new_row))

    with open('results.txt', 'w') as f:
        # Write manually implemented rowss
        f.write("Baseline Data Length\n")
        f.write(f"{input_baseline_data.shape[0]}\n")
        f.write("Rows Removed\tRMSSD\tRMSE\tMean\tSampEn\n")
        f.write(f"0\t{baseline_rmssd}\t{baseline_rmse}\t{baseline_mean}\t{baseline_sampen}\n")

        f.write("Original Data Length\n")
        f.write(f"{input_condition_data.shape[0]}\n")
        f.write("Rows Removed\tRMSSD\tRMSE\tMean\tSampEn\n")
        f.write(f"0\t{original_condition_rmssd}\t{original_conditon_rmse}\t{original_condition_mean}\t{original_condition_sampen}\n")
        
        # Write numpy array to text file
        np.savetxt(f, output,delimiter='\t')
        print("Data saved")

#Calcuates each measure and creates a row from them. Adds the number of removed rows to the start
def calculate_and_write(intervals,eliminated):
    final_rmssd = s.calculate_rmssd(intervals)
    final_rmse = s.calculate_rmse(intervals)
    final_mean = s.mean_interval(intervals)
    final_sampen = s.calculate_sampen(intervals)
    new_row = [eliminated,final_rmssd,final_rmse,final_mean,final_sampen]
    return new_row

#Randonmly deletes n RRIs from the dataset
def rand_delete(data,max_removed):
    maximum = int(max_removed*data.shape[0])
    
    eliminated = random.randint(1,maximum)
    curr_data = data

    counter = 0 
    while counter < eliminated: 
        rand_pos = random.randint(0,len(curr_data)-1)
        curr_data = np.delete(curr_data,rand_pos,axis=0)
        counter += 1

    return curr_data, eliminated
    

if __name__ == '__main__':
    main()
