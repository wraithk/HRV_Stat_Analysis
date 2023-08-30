import numpy as np
import random
import stats_calculator as s
import csv


def main():
    participants = [1,2,3,4,5,6,8]
    csv_data = []
    header = ['% Removed', ' ']
    for i in participants:
        header.extend([f'P{i} RMSSD', f'P{i} RMSE', f'P{i} Mean', f'P{i} SampEn',f'P{i} D2',''])
    csv_data.append(header)

    baseline_output = ["0",' ']
    for i in participants:
        #Import baseline and conditions R Peaks data
        input_baseline_data = np.genfromtxt(f'Data/P{i}/baseline_ECG_R-Peaks.txt', delimiter='\t')
        
        baseline_intervals = calculate_r_r_intervals(input_baseline_data)
        np.savetxt(f"P{i}_baseline_intervals.txt",baseline_intervals)
        #Calculate the HRV measures of the baseline 
        baseline_row = calculate_and_write(baseline_intervals)
        baseline_output.extend(baseline_row)
        baseline_output.extend(' ')

    csv_data.append(["Baseline"])
    csv_data.append(baseline_output)

    condition_output = ["0",' ']
    for i in participants: 
        #Import baseline and conditions R Peaks data
        try:
            input_condition_data = np.genfromtxt(f'Data/P{i}/condition_ECG3_R-Peaks_13.99-18.99.txt', delimiter='\t')
        except(FileNotFoundError):
            input_condition_data = np.genfromtxt(f'Data/P{i}/condition_ECG3_R-Peaks_14.0-19.0.txt', delimiter='\t')
        
        condition_intervals = calculate_r_r_intervals(input_condition_data)
        #Calculate the HRV measures of the baseline 
        condition_row = calculate_and_write(condition_intervals)
        condition_output.extend(condition_row)
        condition_output.extend(' ')

    csv_data.append(["Condition"])
    csv_data.append(condition_output)

    counter = 0 
    while counter < 10:
        print(counter)
        curr_row = []
        percent_deleted = random.uniform(0.01, 0.1)
        curr_row.extend([percent_deleted*100])
        curr_row.extend(' ')
        for i in participants: 
        #Import baseline and conditions R Peaks data
            try:
                input_condition_data = np.genfromtxt(f'Data/P{i}/condition_ECG3_R-Peaks_13.99-18.99.txt', delimiter='\t')
            except(FileNotFoundError):
                input_condition_data = np.genfromtxt(f'Data/P{i}/condition_ECG3_R-Peaks_14.0-19.0.txt', delimiter='\t')
            original_condition_intervals = calculate_r_r_intervals(input_condition_data)
            deleted_intervals = rand_delete(original_condition_intervals,percent_deleted)
            new_row = calculate_and_write(deleted_intervals)
            
            curr_row.extend(new_row)
            curr_row.extend(' ')

        csv_data.append(curr_row)
        counter += 1

    with open('Results/All_Participants_Results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

#Calcuates each measure and creates a row from them. Adds the number of removed rows to the start
def calculate_and_write(intervals):
    rmssd = s.calculate_rmssd(intervals)
    rmse = s.calculate_rmse(intervals)
    mean = s.mean_interval(intervals)
    sampen = s.calculate_sampen(intervals)
    d2 = s.calculate_d2(intervals)
    new_row = [rmssd,rmse,mean,sampen,d2]
    return new_row

# Calculates RRIs from the R Peaks data
def calculate_r_r_intervals(data):
    times = data[:,0]
    r_r_intervals = np.diff(times).astype(float) * 1000.00
    return r_r_intervals

#Randonmly deletes n RRIs from the dataset
def rand_delete(data,portion_removed):
    
    eliminated = len(data)*portion_removed
    curr_data = data

    counter = 0 
    while counter < eliminated: 
        rand_pos = random.randint(0,len(curr_data)-1)
        curr_data = np.delete(curr_data,rand_pos,axis=0)
        counter += 1

    return curr_data
    

if __name__ == '__main__':
    main()