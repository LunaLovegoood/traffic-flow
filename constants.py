import convertor as conv
import generator as gen
import physics as phys

# General constants
number_of_vehicles = 500
number_of_lanes = 2
road_interval = conv.km_to_m(2.5) #(km/h)
unit_length = 25
vehicle_length = 2.0 #(m)
max_number_of_vehicles = (road_interval*number_of_lanes) / vehicle_length
average_number_of_vehicles = max_number_of_vehicles * 0.5

# Time constants
number_of_time_stamps = 100
time_step = 2.0 #(s)

# Speed constants
mean_speed = conv.km_per_h_to_m_per_sec(55.0) #(km/h)
speed_deviation = conv.km_per_h_to_m_per_sec(10.0) #(km/h)

# Density constants
max_density = phys.max_density(number_of_lanes, vehicle_length)
tabled_density_values = gen.generate_tabled_density_values(max_density)

# Generate time stamps and distances
time_stamps = gen.generate_time_stamps(number_of_time_stamps, time_step)