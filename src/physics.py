# Traffic flow
#
# Copyright (c) 2018 Yurii Khomiak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np

#
# Velocity functions
#

def calculate_velocities(vehicle_distances, time_step) :
  """ Обчислює значення швидкостей, які залежать від авто та від моменту часу """
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
  """ Обчислює середні значення швидкостей в кожен даний момент часу """
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
  """ Обчислює середню швидкість """
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
  """ Обчислює максимальне значення густини """
  return number_of_lanes / vehicle_length

def calculate_densities(vehicle_distances, road_interval, number_of_lanes, vehicle_length, 
    starting_positions, unit_length) :
  """ Обчислює значення густини в кожен момент часу на кожному інтервалі довжини заданої параметром unit_length """
  densities = np.zeros((int(road_interval/unit_length), vehicle_distances.shape[1]))
  total_length_of_unit_length = unit_length * number_of_lanes

  positions = np.copy(starting_positions)
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
    positions = np.copy(starting_positions)
    current_position = 0

  return densities

def number_of_vehicles_in_the_interval(positions, lower_bound, upper_bound) :
  """ Обчислює ксть авто в заданому інтервалі в певний момент часу """
  number_of_vehicles = 0

  for i in range(0, positions.size) :
    if is_inside_interval(positions[i], lower_bound, upper_bound) :
      number_of_vehicles += 1
  
  return number_of_vehicles

def is_inside_interval(value, lower_bound, upper_bound) :
  """ Визначає чи є заданий автомобіль в заданому інтервалі  """
  return (value >= lower_bound and value < upper_bound)

def update_positions(positions, vehicle_distances, time_moment) :
  """ Оновлює позиції автомобілів """
  updated_positions = positions

  for i in range(0, updated_positions.size) :
    updated_positions[i] = positions[i] + vehicle_distances[i][time_moment]

  return updated_positions

def calculate_mean_densities(densities) :
  """ Обчислює середні значення густини в кожен даний момент часу """
  mean_densities = np.zeros(densities.shape[1])
  number_of_non_zero_densities = 0

  for time_moment in range(0, mean_densities.size) :
    for interval_index in range(0, densities.shape[0]) :
      if densities[interval_index][time_moment] != 0 :
        mean_densities[time_moment] += densities[interval_index][time_moment]
        number_of_non_zero_densities += 1
    if number_of_non_zero_densities != 0 :
      mean_densities[time_moment] /= number_of_non_zero_densities
    number_of_non_zero_densities = 0

  return mean_densities

def calculate_mean_density(mean_densities) :
  """ Обчислює середнє значення густини """
  mean_density = 0
  number_of_non_zero_densities = 0

  for i in range(0, mean_densities.size) :
    if mean_densities[i] != 0 :
      mean_density += mean_densities[i]
      number_of_non_zero_densities += 1

  if number_of_non_zero_densities != 0 :
    mean_density /= number_of_non_zero_densities
  return mean_density

#
# Flow rate functions
#

def calculate_flow_rates(mean_velocities, densities) :
  """ Обчислює значення потоку в кожен момент часу на кожному інтервалі дороги """
  flow_rates = np.zeros(densities.shape)

  for time_moment in range(0, flow_rates.shape[1]) :
    for interval_index in range(0, flow_rates.shape[0]) :
      flow_rates[interval_index][time_moment] = densities[interval_index][time_moment] * mean_velocities[time_moment]

  return flow_rates

def calculate_mean_flow_rates(flow_rates) :
  """ Обчислює середні значення потоку в кожен даний момент часу """
  mean_flow_rates = np.zeros(flow_rates.shape[1])

  for time_moment in range(0, flow_rates.shape[1]) :
    for interval_index in range(0, flow_rates.shape[0]) :
        mean_flow_rates[time_moment] += flow_rates[interval_index][time_moment]
    mean_flow_rates[time_moment] /= mean_flow_rates.size

  return mean_flow_rates

def calculate_mean_flow_rate(mean_flow_rates) :
  """ Обчислює середнє значення потоку """
  mean_flow_rate = 0

  for i in range(0, mean_flow_rates.size) :
    mean_flow_rate += mean_flow_rates[i]

  mean_flow_rate /= mean_flow_rates.size
  return mean_flow_rate

def calculate_deduced_flow_rates(densities, max_velocity, max_density) :
  """ Обчислює значення потоку для побудови фундаментальної діаграми """
  flow_rates = np.zeros(densities.size)

  for i in range(0, flow_rates.size) :
    flow_rates[i] = max_velocity * ( densities[i] - ((densities[i]**2) / max_density) )

  return flow_rates

