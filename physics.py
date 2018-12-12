import numpy as np

def calculate_velocities(vehicle_distances, time_step) :
    rows, cols = vehicle_distances.shape
    velocities = np.zeros((rows, cols))
    number_of_non_zero_velocities = 0

    for i in range(0, rows) :
        for j in range(0, cols) :
            if vehicle_distances[i][j] != 0 :
                velocities[i][j] = vehicle_distances[i][j] / time_step
                number_of_non_zero_velocities += 1

    plane_velocities = np.zeros(number_of_non_zero_velocities)
    index = 0

    for i in range(0, rows) :
        for j in range(0, cols) :
            if velocities[i][j] != 0 :
                plane_velocities[index] = velocities[i][j]
                index += 1

    return [velocities, plane_velocities]

def calculate_mean_velocities(velocities) :
    rows, cols = velocities.shape
    mean_velocities = np.zeros(rows)
    number_of_non_zero_velocities = 0

    for i in range(0, rows) :
        for j in range(0, cols) :
            if velocities[i][j] != 0 :
                mean_velocities[i] += velocities[i][j]
                number_of_non_zero_velocities += 1
        mean_velocities[i] /= number_of_non_zero_velocities
        number_of_non_zero_velocities = 0

    return mean_velocities

def calculate_mean_velocity(mean_velocities) :
    mean_velocity = 0

    for i in range(0, mean_velocities.size) :
        mean_velocity += mean_velocities[i]
    mean_velocity /= mean_velocities.size

    return mean_velocity
