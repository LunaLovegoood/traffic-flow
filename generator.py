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
    average_number_of_vehicles) :
  number_of_time_stamps = time_stamps.size
  time_step = time_stamps[1] - time_stamps[0]
  mean_speed *= time_step
  speed_deviation *= time_step
  shift = 2.0

  distances = np.zeros((number_of_vehicles, number_of_time_stamps))
  starting_positions = generate_starting_positions(number_of_vehicles, average_number_of_vehicles, 
      vehicle_length, road_interval, number_of_lanes)
  positions = np.copy(starting_positions)

  first_unexistent_vehicle_index = find_first_unexistent_vehicle(positions)

  for i in range(0, number_of_time_stamps) :
    if first_unexistent_vehicle_index < number_of_vehicles :
      first_unexistent_vehicle_index += int(np.random.uniform(0, number_of_lanes + 1))
      if first_unexistent_vehicle_index > number_of_vehicles :
        first_unexistent_vehicle_index = number_of_vehicles
    for j in range(0, first_unexistent_vehicle_index) :
      if positions[j] == road_interval :
        continue
      gamma_shift = np.random.gamma(9, 0.5) - 2.0
      distances[j][i] = np.random.normal(mean_speed, speed_deviation) + gamma_shift - shift
      if distances[j][i] < 0 :
        distances[j][i] = 0
      if (positions[j] + distances[j][i]) <= road_interval :
        positions[j] += distances[j][i]
      else :
        distances[j][i] = road_interval - positions[j]
        positions[j] = road_interval

  return [distances, positions, starting_positions]

def generate_starting_positions(number_of_vehicles, average_number_of_vehicles,
    vehicle_length, road_interval, number_of_lanes) :
  starting_positions = np.zeros(number_of_vehicles)
  mean_spacing = ((road_interval*number_of_lanes) - (vehicle_length*average_number_of_vehicles)) / average_number_of_vehicles

  for i in range(0, number_of_vehicles, number_of_lanes) :
    for j in range(0, number_of_lanes) :
      if (i + j) >= number_of_vehicles :
        break
      position_shift = np.random.normal(mean_spacing, mean_spacing*0.2)
      position_shift = position_shift if (position_shift >= 0) else 0
      if (i - number_of_lanes) >= 0 :
        position = starting_positions[i - number_of_lanes] + position_shift
      else :
        position = position_shift
      starting_positions[i + j] = position if (position <= road_interval) else 0
  
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

def generate_tabled_density_values(max_density) :
  step = 0.001
  return np.arange(0, max_density + step, step)

