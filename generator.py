import numpy as np

def generate_time_intervals(number_of_time_points, time_step) :
    if (number_of_time_points <= 0 or time_step <= 0) :
        return np.array([])
    time_intervals = np.arange(0, number_of_time_points * time_step, time_step)
    return time_intervals

