import numpy as np

#
# Velocity functions
#

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
        if number_of_non_zero_velocities != 0 :
            mean_velocities[i] /= number_of_non_zero_velocities
        number_of_non_zero_velocities = 0

    return mean_velocities

def calculate_mean_velocity(mean_velocities) :
    mean_velocity = 0

    for i in range(0, mean_velocities.size) :
        mean_velocity += mean_velocities[i]
    mean_velocity /= mean_velocities.size

    return mean_velocity

#
# Density functions
#

def max_density(number_of_lanes, vehicle_length) :
    return number_of_lanes / vehicle_length

def density(vehicle_distances, t, total_length, vehicle_length) :
    density_value = 0
    space_occupied_by_vehicles = 0

    for i in range(0, vehicle_distances.shape[0]) :
        if vehicle_distances[i][t] != 0 :
            space_occupied_by_vehicles += vehicle_length + 0.4

    density_value = space_occupied_by_vehicles / total_length
    return density_value

def calculate_total_length(road_interval, number_of_lanes) :
    return road_interval * number_of_lanes

def calculate_densities(vehicle_distances, road_interval, number_of_lanes, vehicle_length) :
    densities = np.zeros(vehicle_distances.shape[1])
    total_length = calculate_total_length(road_interval, number_of_lanes)

    for i in range(0, densities.size) :
        densities[i] = density(vehicle_distances, i, total_length, vehicle_length)

    return densities

def calculate_mean_density(densities) :
    mean_density = 0

    for i in range(0, densities.size) :
        mean_density += densities[i]

    mean_density /= densities.size
    return mean_density

#
# Flow rate functions
#

def calculate_flow_rates(mean_velocities, densities) :
    flow_rates = np.zeros(densities.size)

    for i in range(0, flow_rates.size) :
        flow_rates[i] = densities[i] * mean_velocities[i]

    return flow_rates

def calculate_mean_flow_rate(flow_rates) :
    mean_flow_rate = 0

    for i in range(0, flow_rates.size) :
        mean_flow_rate += flow_rates[i]

    mean_flow_rate /= flow_rates.size
    return mean_flow_rate


