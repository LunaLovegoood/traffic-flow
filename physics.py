import numpy as np

#
# Velocity functions
#

def calculate_velocities(vehicle_distances, time_step) :
  rows, cols = vehicle_distances.shape
  velocities = np.zeros((rows, cols))
  number_of_vehicles = 0

  for i in range(0, rows) :
    for j in range(0, cols) :
      if vehicle_distances[i][j] != 0 :
        velocities[i][j] = vehicle_distances[i][j] / time_step
        number_of_vehicles += 1

  plane_velocities = np.zeros(number_of_vehicles)
  index = 0

  for i in range(0, rows) :
    for j in range(0, cols) :
      if velocities[i][j] != 0 :
        plane_velocities[index] = velocities[i][j]
        index += 1

  return [velocities, plane_velocities]

def calculate_mean_velocities(velocities) :
  rows, cols = velocities.shape
  mean_velocities = np.zeros(cols)
  number_of_vehicles = 0

  for j in range(0, cols) :
    for i in range(0, rows) :
      if velocities[i][j] != 0 :
        mean_velocities[j] += velocities[i][j]
        number_of_vehicles += 1
    if number_of_vehicles != 0 :
      mean_velocities[j] /= number_of_vehicles
    number_of_vehicles = 0

  return mean_velocities

def calculate_mean_velocity(mean_velocities) :
  mean_velocity = 0
  number_of_vehicles = 0

  for i in range(0, mean_velocities.size) :
    if mean_velocities[i] != 0 :
      mean_velocity += mean_velocities[i]
      number_of_vehicles += 1

  if number_of_vehicles != 0 :
    mean_velocity /= number_of_vehicles

  return mean_velocity

#
# Density functions
#

def max_density(number_of_lanes, vehicle_length) :
  return number_of_lanes / vehicle_length

def calculate_densities(vehicle_distances, road_interval, number_of_lanes, vehicle_length, 
    starting_positions, unit_length) :
  densities = np.zeros((int(road_interval/unit_length), vehicle_distances.shape[1]))
  total_length_of_unit_length = unit_length * number_of_lanes

  positions = starting_positions
  current_position = 0

  for time_moment in range(0, densities.shape[1]) :
    for interval_index in range(0, densities.shape[0]) :
      densities[interval_index][time_moment] = number_of_vehicles_in_the_interval(
          positions,
          current_position, current_position + unit_length)
      if densities[interval_index][time_moment] != 0 :
        densities[interval_index][time_moment] = (densities[interval_index][time_moment]*vehicle_length) / total_length_of_unit_length
      positions = update_positions(positions, vehicle_distances, time_moment)
      current_position += unit_length
    positions = starting_positions
    current_position = 0

  return densities

def number_of_vehicles_in_the_interval(positions, lower_bound, upper_bound) :
  number_of_vehicles = 0

  for i in range(0, positions.size) :
    if is_inside_interval(positions[i], lower_bound, upper_bound) :
      number_of_vehicles += 1

  return number_of_vehicles

def is_inside_interval(value, lower_bound, upper_bound) :
  return (value >= lower_bound and value <upper_bound)

def update_positions(positions, vehicle_distances, time_moment) :
  updated_positions = positions

  for i in range(0, updated_positions.size) :
    updated_positions[i] = positions[i] + vehicle_distances[i][time_moment]

  return updated_positions

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

def calculate_deduced_flow_rates(densities, max_velocity, max_density) :
  flow_rates = np.zeros(densities.size)

  for i in range(0, flow_rates.size) :
    flow_rates[i] = max_velocity * ( densities[i] - ((densities[i]**2) / max_density) )

  return flow_rates

