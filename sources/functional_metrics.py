# This script uses part of Victor Fernando Lopes De Souza's script.

import numpy as np

## Defining Metrics

"""
### Jerk
$J_i(t)=\frac{a_i(t+d t)-a_i(t-d t)}{2 d t}$
"""
def get_jerk(acceleration_xyzn, time_index):
    delta_t = np.mean(time_index[2:] - time_index[:-2])
    jerk_xyz = (acceleration_xyzn[2:, :, 0:3] - acceleration_xyzn[:-2, :, 0:3]) / (2 * delta_t)
    jerk_norm = np.linalg.norm(jerk_xyz, axis=2)
    jerk_norm = jerk_norm.reshape(jerk_norm.shape[0], jerk_norm.shape[1], 1)

    jerk = np.concatenate((jerk_xyz, jerk_norm), axis=2)

    return jerk



"""
### Jerk ratio
$\operatorname{Jerk}_{\text {Ratio }}=2 x \frac{\mid \text { Jerk }_{\text {paretic }} \mid}{\mid \text { Jerk }_{\text {pareetic }}|+| \text { Jerk }_{\text {non-paretic }}|}$
"""
get_ratio = lambda non_paretic, paretic : 2 * paretic / (non_paretic + paretic)

def get_jerk_ratio(jerk, treshold_removal=0):
    jerk_paretic = np.abs(jerk[:, 1, 3])
    jerk_non_paretic = np.abs(jerk[:, 0, 3])

    # get indexes where some of the jerks is lower than the treshold
    idx = np.where((jerk_paretic < treshold_removal) | (jerk_non_paretic < treshold_removal))

    # remove the indexes
    jerk_paretic = np.delete(jerk_paretic, idx)
    jerk_non_paretic = np.delete(jerk_non_paretic, idx)
    
    return get_ratio(jerk_non_paretic, jerk_paretic)
    


"""
### Alpha
$\alpha(t)=\operatorname{arcos}\left(\frac{a_y(t)}{E N(t)}\right)$
"""
get_alphas = lambda a_y, EN : np.arccos(a_y / EN) - np.deg2rad(90)



"""
### Functional Count 
Functional: $|\alpha| \leq 30^{\circ} \text { and } \alpha_{\text {max }}-\alpha_{\text {min }} \geq 30^{\circ} $
"""

def get_functional_count_per_day(is_functional, time_indexes):
    """
    Calculates the number of functional movements per day.

    This function counts the number of functional movements that start each day based on the provided 
    `is_functional` array and time index. Each row in the output represents a day, and each column 
    represents an arm.

    Parameters
    -----------
    is_functional : numpy.ndarray
        2D array where each entry indicates if a movement is functional (1) or not (0) for each arm 
        and time point.

    time_indexes : numpy.ndarray
        2D array of time indices for each window.

    Returns
    --------
    functional_count_day : numpy.ndarray
        2D array where each row represents a day and each column represents an arm, with the count 
        of functional movements that started on that day.
    """
    # get first element of each window
    start = time_indexes[:, 0]
    
    # get differences
    delta_windowing = np.diff(start).mean()
    
    # get the second when each window starts
    time_after_beginning = np.cumsum(delta_windowing * np.ones(start.shape[0]))
    second_of_measurement = np.floor(time_after_beginning).astype(int)

    # convert seconds to days
    day_of_measurement = second_of_measurement // (24 * 3600)

    # one row per day, one column per arm
    functional_count_day = np.zeros((day_of_measurement[-1] + 1, is_functional.shape[1]))
    
    # the functional count in each day is the number of functional movements that started in that day
    for i in range(is_functional.shape[0]):
        for j in range(is_functional.shape[1]):
            functional_count_day[day_of_measurement[i], j] += is_functional[i, j]

    return functional_count_day



def test_functional(alphas, treshold_symregion_degrees=30, treshold_amp_degrees=30):
    """ 
    Tests if a movement in each epoch (window) is functional based on symmetry and amplitude thresholds.

    This function evaluates whether the movement in each epoch meets the criteria for being considered 
    functional based on the symmetry and amplitude of the movement.

    Parameters
    -----------
    alphas : numpy.ndarray
        2D array where each row represents an epoch (window) and each column represents a different angle.
    
    treshold_symregion_degrees : float, optional (default=30)
        The threshold for symmetry in degrees. All absolute values in the epoch should be less than or equal to this threshold.

    treshold_amp_degrees : float, optional (default=30)
        The threshold for the amplitude in degrees. The range (max - min) in the epoch should be greater than or equal to this threshold.

    Returns
    --------
    numpy.ndarray
        Boolean array where each entry is `True` if the corresponding epoch represents a functional movement, 
        and `False` otherwise. 
    """

    threshold_amp_radians = np.deg2rad(treshold_amp_degrees)
    treshold_symregion_radians = np.deg2rad(treshold_symregion_degrees)

    # All absolute values in each epoch (row here) should be less than or equal to the threshold
    condition1 = (np.abs(alphas) <= treshold_symregion_radians).all(axis=1)
    # The range (max - min) in each epoch (row here) should be greater than or equal to the threshold
    condition2 = (alphas.max(axis=1) - alphas.min(axis=1)) >= threshold_amp_radians
    is_functional = condition1 & condition2

    return is_functional



"""
### Use Hours
# The total hours of use is the total amount of time, in hours, as measured by summing the seconds when the activity count was > 0
"""
def get_use_hours(is_functional, time_indexes, activity_treshold=0):
    # get first element of each window
    start = time_indexes[:, 0]
    
    # get differences
    delta_windowing = np.diff(start).mean()
    
    # get the second when each window starts
    time_after_beginning = np.cumsum(delta_windowing * np.ones(start.shape[0]))
    second_of_measurement = np.floor(time_after_beginning).astype(int)

    # one row per second, one column per arm
    activity_count_second = np.zeros((second_of_measurement[-1] + 1, is_functional.shape[1]))
    
    # the activity in each second is the number of functional movements that started in that second
    for i in range(is_functional.shape[0]):
        for j in range(is_functional.shape[1]):
            activity_count_second[second_of_measurement[i], j] += is_functional[i, j]

    is_active_second = activity_count_second > activity_treshold
    use_seconds = is_active_second.sum(axis=0)

    return use_seconds / 3600
