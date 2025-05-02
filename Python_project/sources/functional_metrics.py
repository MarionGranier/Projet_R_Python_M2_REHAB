# This script uses part of Victor Fernando Lopes De Souza's script.

import numpy as np


## Defining Metrics


def get_ratio(non_paretic: float, paretic: float) -> float:
    """
    Compute the ratio of functional use between paretic and non-paretic limbs.

    Parameters
    ----------
    non_paretic : float
        Functional count for the non-paretic limb.
    
    paretic : float
        Functional count for the paretic limb.

    Returns
    -------
    float
        Ratio: 2 * paretic / (paretic + non_paretic)
    """
    return 2 * paretic / (non_paretic + paretic)


def get_angle_from_horizontal(a_y, EN):
    """
    Computes the elevation angle (alpha) of the forearm relative to the gravity vector 
    in quasi-static conditions.

    According to trigonometric laws [Fisher, C. J. (2010)], the angle is given by:

        α(t) = arccos(a_y(t) / EN(t))

    Parameters:
    -----------
    a_y : np.ndarray
        Acceleration data along the forearm axis (y-axis) at a given time t.
    
    EN : np.ndarray
        Euclidean Norm (magnitude) of the acceleration vector at a given time t.

    Returns:
    --------
    np.ndarray
        The computed elevation angle α(t) in radians.
    """
    return np.arccos(a_y/EN) - np.pi/2  # Converts from [0, π] to [-π/2, π/2]


def get_functional_count_per_day(is_functional, time_indexes):
    """
    Calculates the number of functional movements per day.

    This function counts the number of functional movements that start each day based on the provided 
    `is_functional` array and time index. Each row in the output represents a day, and each column 
    represents an arm.  

    Functional movements are defined by: 
        ∣α(t)∣ ≤ 30° et αmax − αmin ≥ 30°

    Parameters
    -----------
    is_functional : np.ndarray
        2D array where each entry indicates if a movement is functional (1) or not (0) for each arm 
        and time point.

    time_indexes : np.ndarray
        2D array of time indices for each window.

    Returns
    --------
    functional_count_day : np.ndarray
        2D array where each row represents a day and each column represents an arm, with the count 
        of functional movements that started on that day.
    """
    # Get first element of each window
    start = time_indexes[:, 0]
    
    # Get differences
    delta_windowing = np.diff(start).mean()
    
    # Get the second when each window starts
    time_after_beginning = np.cumsum(delta_windowing * np.ones(start.shape[0]))
    second_of_measurement = np.floor(time_after_beginning).astype(int)

    # Convert seconds to days
    day_of_measurement = second_of_measurement // (24*3600)

    # One row per day, one column per arm
    functional_count_day = np.zeros((day_of_measurement[-1] + 1, is_functional.shape[1]))
    
    # The functional count in each day is the number of functional movements that started in that day
    for i in range(is_functional.shape[0]):
        for j in range(is_functional.shape[1]):
            functional_count_day[day_of_measurement[i], j] += is_functional[i, j]

    return functional_count_day


def test_functional(alphas, threshold_symregion_degrees=30, threshold_amp_degrees=30):
    """ 
    Tests if a movement in each epoch (window) is functional based on symmetry and amplitude thresholds.

    This function evaluates whether the movement in each epoch meets the criteria for being considered 
    functional based on the symmetry and amplitude of the movement.

    Parameters
    -----------
    alphas : np.ndarray
        2D array where each row represents an epoch (window) and each column represents a different angle.
    
    threshold_symregion_degrees : float, optional (default=30)
        The threshold for symmetry in degrees. All absolute values in the epoch should be less than or equal to this threshold.

    threshold_amp_degrees : float, optional (default=30)
        The threshold for the amplitude in degrees. The range (max - min) in the epoch should be greater than or equal to this threshold.

    Returns
    --------
    np.ndarray
        Boolean array where each entry is `True` if the corresponding epoch represents a functional movement, 
        and `False` otherwise. 
    """

    threshold_amp_radians = np.deg2rad(threshold_amp_degrees)
    threshold_symregion_radian = np.deg2rad(threshold_symregion_degrees)

    # All absolute values in each epoch (row here) should be less than or equal to the threshold
    condition1 = (np.abs(alphas) <= threshold_symregion_radian).all(axis=1)
    # The range (max - min) in each epoch (row here) should be greater than or equal to the threshold
    condition2 = (alphas.max(axis=1) - alphas.min(axis=1)) >= threshold_amp_radians
    is_functional = condition1 & condition2

    return is_functional
