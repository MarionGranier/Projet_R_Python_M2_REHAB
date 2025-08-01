# This script uses part of Victor Fernando Lopes De Souza's script.

import numpy as np
import pandas as pd

from scipy.signal import butter, filtfilt

act_folder = 'data/data_actimetry/'


def extract_data(session, filter_butter_cutoff=1, resampling_freq=50, month=None):
    """
    Extract and preprocess data from the given session.

    This function loads the participant's data, applies resampling and low-pass filtering, and returns
    time-indexed acceleration data for both paretic and non-paretic arms.

    Parameters
    -----------
    session : str
        The session identifier for the participant's data.
    
    filter_butter_cutoff : float, optional (default=1)
        The cutoff frequency for the Butterworth low-pass filter in Hz.

    resampling_freq : int, optional (default=50)
        The frequency (Hz) to resample the data to.

    month : str, optional
        The month used to specify the participant's data file.

    Returns
    --------
    time_index : pandas.DatetimeIndex
        The time index for the data.
    
    acceleration_xyzn : np.ndarray
        3D array of acceleration data for both paretic and non-paretic sides (timepoints, arms, axes).
    
    is_patient : bool
        Indicates whether the participant is a patient.

    FMScore : float
        The Fugl-Meyer Score of the participant.
    """
    if month is None:
        raise ValueError("Month must be specified for data extraction.")

    # Get the folder name
    folder_name = act_folder + session

    # Get the participant's information
    participants_info = pd.read_csv(f'data/participants_{month}.csv', sep=';')
    volunteer_info = participants_info[participants_info['folder_name'] == session]
    is_patient = volunteer_info['is_patient'].values[0]
    FMScore = volunteer_info['FMScore'].values[0]

    # Get the paretic and non-paretic side
    paretic_side = volunteer_info['paretic_side'].values[0]
    non_paretic_side = 'left' if paretic_side == 'right' else 'right'

    def get_arm_data(side):
        # Read the arm data
        arm_data = pd.read_csv(folder_name + '/' + side + '.csv', sep=',', header=None)
        arm_data.columns = ['timestamp', 'x', 'y', 'z']
        arm_data['timestamp'] = pd.to_datetime(arm_data['timestamp'])
        arm_data.set_index('timestamp', inplace=True)
        
        # Resample the data if needed
        if resampling_freq is not None:
            resample = f'{int(1000/resampling_freq)}ms'
            arm_data = arm_data.resample(resample).mean().interpolate()

        # Apply a low-pass filter if needed
        if filter_butter_cutoff is not None:
            delta_t = np.diff(arm_data.index).mean() / np.timedelta64(1, 's')
            for i in arm_data.columns:
                arm_data[i] = butter_filter(arm_data[i], delta_t, filter_butter_cutoff)

        # Calculate the norm of the acceleration
        arm_data['norm'] = np.linalg.norm(arm_data[['x', 'y', 'z']], axis=1)

        return arm_data
    
    # Get the arm data for the paretic and non-paretic side
    paretic_data = get_arm_data(paretic_side)
    non_paretic_data = get_arm_data(non_paretic_side)

    # Remove the beginning of the earlier dataset to make the start times match
    start = max(paretic_data.index[0], non_paretic_data.index[0])
    paretic_data = paretic_data[start:]
    non_paretic_data = non_paretic_data[start:]
    
    # Remove the end of the longer dataset to make the lengths match
    length = min(paretic_data.shape[0], non_paretic_data.shape[0])
    paretic_data = paretic_data[:length]
    non_paretic_data = non_paretic_data[:length]

    time_index = paretic_data.index
    acceleration_xyzn = np.stack([non_paretic_data.values, paretic_data.values], axis=1)
    return time_index, acceleration_xyzn, is_patient, FMScore


def butter_filter(time_series, delta_t, cutoff):
    """
    Apply a low-pass Butterworth filter to a time series with a cutoff frequency of 50 Hz by default.

    Parameters:
        time_series (np.ndarray): The input time series data.
        delta_t (float): The time step between consecutive samples.
        cutoff (float): The cutoff frequency for the low-pass filter (default is 50 Hz).

    Returns:
        np.ndarray: The filtered time series.
    """
    # Calculate the Nyquist frequency
    nyquist = 0.5 / delta_t
    
    # Ensure cutoff frequency is below the Nyquist
    if cutoff >= nyquist:
        raise ValueError("Cutoff frequency must be less than the Nyquist frequency.")
    
    # Design the Butterworth filter
    b, a = butter(N=4, Wn=cutoff / nyquist, btype='low', analog=False)
    
    # Apply the filter
    filtered_series = filtfilt(b, a, time_series)
    
    return filtered_series


def partition(acceleration_xyzn, time_index, seconds_per_window=5):
    """
    Partitions acceleration data and time index into time windows.

    This function splits the acceleration data and corresponding time index into smaller segments 
    based on a specified window duration in seconds.

    Parameters
    -----------
    acceleration_xyzn : np.ndarray
        3D array of acceleration data (n_timepoints, n_arms, n_axes).
    
    time_index : np.ndarray
        1D array of time points corresponding to the acceleration data.
    
    seconds_per_window : int, optional (default=5)
        Duration of each time window in seconds.

    Returns
    --------
    acceleration_xyzn : np.ndarray
        4D array of acceleration data partitioned into time windows (n_windows, window_size, n_arms, n_axes).
    
    time_index : np.ndarray
        2D array of time indices for each window (n_windows, window_size).
    """
    # Calculate sampling interval
    delta_t = float(np.diff(time_index).mean())

    # Get data shape
    number_timepoints = acceleration_xyzn.shape[0]
    number_arms = acceleration_xyzn.shape[1]
    number_axis = acceleration_xyzn.shape[2]

    # Compute window size and number of windows
    window_size = int(seconds_per_window / delta_t)
    num_windows = number_timepoints // window_size

    # Truncate and reshape the data
    acceleration_xyzn = acceleration_xyzn[:num_windows * window_size]
    acceleration_xyzn = acceleration_xyzn.reshape(
        (num_windows, window_size, number_arms, number_axis)
    )

    # Partition time index
    time_index = time_index[:num_windows * window_size]
    time_index = time_index.reshape((num_windows, window_size))
    
    return acceleration_xyzn, time_index
