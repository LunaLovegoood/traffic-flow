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

from constants import *
import generator as gen
import convertor as conv
import physics as phys
import output_manager as out_mng
import plotter

# Отримуємо величини змін положень авто на відрізку дороги, а також їх кінцеві та початкові позиції
vehicle_distances, positions, starting_positions = gen.generate_distances(
    number_of_vehicles, number_of_lanes, vehicle_length, 
    road_interval, time_stamps, 
    mean_speed, speed_deviation,
    average_number_of_vehicles
  )

#
# Обчислення
#

# Обчислюємо швидкості та їх середні значення
velocities, plane_velocities = phys.calculate_velocities(vehicle_distances, time_step)
max_velocity = np.amax(velocities)
mean_velocities = phys.calculate_mean_velocities(velocities)
mean_velocity = phys.calculate_mean_velocity(mean_velocities)

# Обчислюємо густини та їх середні значення
densities = phys.calculate_densities(
    vehicle_distances, road_interval, 
    number_of_lanes, vehicle_length, 
    starting_positions, unit_length
  )
mean_densities = phys.calculate_mean_densities(densities)
mean_density = phys.calculate_mean_density(mean_densities)

# Обчислюємо потоки та їх середні значення
flow_rates = phys.calculate_flow_rates(mean_velocities, densities)
mean_flow_rates = phys.calculate_mean_flow_rates(flow_rates)
mean_flow_rate = phys.calculate_mean_flow_rate(mean_flow_rates)
deduced_flow_rates = phys.calculate_deduced_flow_rates(tabled_density_values, max_velocity, max_density)
max_flow_rate = deduced_flow_rates.max()

#
# Виведення результатів
#

out_mng.print_basic_constants(road_interval, number_of_lanes, number_of_vehicles, number_of_time_stamps)
out_mng.print_max_values(max_velocity, max_density, max_flow_rate)
out_mng.print_mean_values(mean_velocity, mean_density, mean_flow_rate)

#
# Створення та виведення графіків
#

plotter.plot_velocity_distribution(plane_velocities)
plotter.plot_fundamental_diagram(tabled_density_values, deduced_flow_rates, mean_densities, mean_flow_rates)
plotter.show_plots()