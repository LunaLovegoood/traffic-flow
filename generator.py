import numpy as np

def generate_time_stamps(number_of_time_stamps, time_step) :
    if number_of_time_stamps <= 0 or time_step <= 0 :
        return np.array([])
    time_stamps = np.arange(0, number_of_time_stamps * time_step, time_step)
    return time_stamps

def generate_distances(
    number_of_vehicles, number_of_lanes, vehicle_length, 
    road_interval, time_stamps, 
    mean_speed, speed_deviation,
    spacing, spacing_scatter) :
    
    number_of_time_stamps = time_stamps.size
    time_step = time_stamps[1] - time_stamps[0]
    mean_speed *= time_step
    speed_deviation *= time_step

    distances = np.zeros((number_of_vehicles, number_of_time_stamps))
    positions = generate_starting_positions(
        number_of_vehicles, road_interval, number_of_lanes,spacing, spacing_scatter)

    first_unexistent_vehicle_index = find_first_unexistent_vehicle(positions)

    for i in range(0, number_of_time_stamps) :
        for _ in range(0, number_of_lanes) :
            if first_unexistent_vehicle_index < number_of_vehicles :
                first_unexistent_vehicle_index += 1
            else :
                break
        for j in range(0, first_unexistent_vehicle_index) :
            if positions[j] == road_interval :
                continue
            distances[j][i] = np.random.normal(mean_speed, speed_deviation)
            if distances[j][i] < 0 :
                distances[j][i] = 0
            if (positions[j] + distances[j][i]) <= road_interval :
                positions[j] += distances[j][i]
            else :
                distances[j][i] = road_interval - positions[j]
                positions[j] = road_interval

    return [distances, positions]

def generate_starting_positions(number_of_vehicles, road_interval, number_of_lanes, 
                                spacing, spacing_scatter) :
    starting_positions = np.zeros(number_of_vehicles)

    for i in range(0, number_of_vehicles, number_of_lanes) :
        for j in range(0, number_of_lanes) :
            position = (spacing * i) + (np.random.random() * spacing_scatter)
            if (i + j) >= number_of_vehicles :
                break
            starting_positions[i + j] = position if (position <= road_interval) else 0.0

    first_unexistent_vehicle_index = find_first_unexistent_vehicle(starting_positions)
    reverse_index = first_unexistent_vehicle_index - 1

    for i in range(0, first_unexistent_vehicle_index) :
        if i >= reverse_index :
            break
        temp = starting_positions[i]
        starting_positions[i] = starting_positions[reverse_index]
        starting_positions[reverse_index] = temp
        reverse_index -= 1

    return starting_positions

def find_first_unexistent_vehicle(starting_positions) :
    vehicle_index = 0
    while vehicle_index < starting_positions.size :
        if starting_positions[vehicle_index] != 0 :
            vehicle_index += 1
        else :
            break
    return vehicle_index

