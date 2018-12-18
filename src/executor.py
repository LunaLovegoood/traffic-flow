import numpy as np

from constants import *
import generator as gen
import convertor as conv
import physics as phys
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
# Виведення базових константних величин моделі
#

print('Базові константи: ')
print('Величина інтервалу дороги: ', conv.m_to_km(road_interval), ' (км)')
print('Кількість смуг дороги: ', number_of_lanes)
print('Кількість автомобілів: ', number_of_vehicles)
print('Кількість часових відліків: ', number_of_time_stamps, end='\n\n')

#
# Виведення обчислених результатів моделі
#

# Виведення максимальних значень величин моделі
print('Максимальні значення:')
print('Максимальне значення швидкості max(v) = ', conv.m_per_sec_to_km_per_h(max_velocity), ' (км/год)')
print('Максимальне значення густини max(густини) = ', max_density, ' (ксть авто/25м)')
print('Максимальне значення потоку max(f) = ', max_flow_rate, ' (авто/с)', end='\n\n')

# Виведення середніх значень величин моделі
print('Середні значення:')
print('Середнє значення швидкості <v> = ', conv.m_per_sec_to_km_per_h(mean_velocity), ' (км/год)')
print('Середнє значення густини <густина> = ', mean_density, ' (ксть авто/25м)')
print('Середнє значення потоку <f> = ', mean_flow_rate, ' (авто/с)', end='\n\n')

#
# Створення та виведення графіків
#

plotter.plot_velocity_distribution(plane_velocities)
plotter.plot_fundamental_diagram(tabled_density_values, deduced_flow_rates, mean_densities, mean_flow_rates)
plotter.show_plots()
