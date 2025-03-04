import numpy as np
import pandas as pd

from scipy.signal import butter, filtfilt

####### ENTER THE MONTH INFORMATION #######
month = "2"
act_folder = '../data/data_actimetry_copy/'
# participants_info = pd.read_csv('../data/participants_' + month + '.csv', sep=';')
participants_info = pd.read_csv('../data/participants_2.csv', sep=';')

def extract_data(session, filter_butter_cutoff=1, resampling_freq=10):
    """
    Extract the data from the given session.
    Preprocess the data by resampling and low-pass (Butterworth) filtering.
    """

    # get the folder name
    folder_name = act_folder + session

    # get the participant's information
    voulonteer_info = participants_info[participants_info['folder_name'] == session]
    is_patient = voulonteer_info['is_patient'].values[0]
    FMScore = voulonteer_info['FMScore'].values[0]

    # get the paretic and non-paretic side
    paretic_side = voulonteer_info['paretic_side'].values[0]
    non_paretic_side = 'left' if paretic_side == 'right' else 'right'

    def get_arm_data(side):
        # read the arm data
        arm_data = pd.read_csv(folder_name + '/' + side + '.csv', sep=',', header=None)
        arm_data.columns = ['timestamp', 'x', 'y', 'z']
        arm_data['timestamp'] = pd.to_datetime(arm_data['timestamp'])
        arm_data.set_index('timestamp', inplace=True)
        
        # resample the data if needed
        if resampling_freq is not None:
            resample = f'{int(1000/resampling_freq)}ms'
            arm_data = arm_data.resample(resample).mean().interpolate()

        # apply a low-pass filter if needed
        if filter_butter_cutoff is not None:
            delta_t = np.diff(arm_data.index).mean() / np.timedelta64(1, 's')
            for i in arm_data.columns:
                arm_data[i] = butter_filter(arm_data[i], delta_t, filter_butter_cutoff)
            arm_data = arm_data

        # calculate the norm of the acceleration
        arm_data['norm'] = np.linalg.norm(arm_data[['x', 'y', 'z']], axis=1)

        return arm_data
    
    # get the arm data for the paretic and non-paretic side
    paretic_data = get_arm_data(paretic_side)
    non_paretic_data = get_arm_data(non_paretic_side)

    # remove the beginning of the earlier dataset to make the start times match
    start = max(paretic_data.index[0], non_paretic_data.index[0])
    paretic_data = paretic_data[start:]
    non_paretic_data = non_paretic_data[start:]
    
    # remove the end of the longer dataset to make the lengths match
    length = min(paretic_data.shape[0], non_paretic_data.shape[0])
    paretic_data = paretic_data[:length]
    non_paretic_data = non_paretic_data[:length]

    time_index = paretic_data.index
    acceleration_xyzn = np.stack([non_paretic_data.values, paretic_data.values], axis=1)
    return time_index, acceleration_xyzn, is_patient, FMScore

def butter_filter(time_series, delta_t, cutoff):
    """
    Apply a low-pass filter to a time series with a cutoff frequency of 50 Hz.

    Parameters:
        time_series (np.ndarray): The input time series data.
        delta_t (float): The time step between consecutive samples.
        cutoff (float): The cutoff frequency for the low-pass filter (default is 50 Hz).

    Returns:
        np.ndarray: The filtered time series.
    """
    # Calculate the Nyquist frequency
    nyquist = 0.5 / delta_t
    
    # Ensure cutoff frequency is below the Nyquist frequency
    if cutoff >= nyquist:
        raise ValueError("Cutoff frequency must be less than the Nyquist frequency.")
    
    # Design the Butterworth filter
    b, a = butter(N=4, Wn=cutoff / nyquist, btype='low', analog=False)
    
    # Apply the filter to the time series
    filtered_series = filtfilt(b, a, time_series)
    
    return filtered_series

def partition(acceleration_xyzn, time_index, seconds_per_window=5):
    # calculate the sampling rate
    delta_t = float(np.diff(time_index).mean())

    # get the dimensions of the data
    number_timepoints = acceleration_xyzn.shape[0]
    number_arms = acceleration_xyzn.shape[1]
    number_axis= acceleration_xyzn.shape[2]

    # partition the data into windows
    window_size = int(seconds_per_window / delta_t)
    num_windows = number_timepoints // window_size

    # truncate the data to fit the windows
    acceleration_xyzn = acceleration_xyzn[:num_windows * window_size]
    acceleration_xyzn = acceleration_xyzn.reshape((num_windows, window_size, number_arms, number_axis))

    # get the time index for each window
    time_index = time_index[:num_windows * window_size]
    time_index = time_index.reshape((num_windows, window_size))
    
    return acceleration_xyzn, time_index