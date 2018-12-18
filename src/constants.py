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

import convertor as conv
import generator as gen
import physics as phys

# Загальні константи
number_of_vehicles = 500
number_of_lanes = 2
road_interval = conv.km_to_m(3.5) #(км/год)
unit_length = 25
vehicle_length = 2.0 #(м)
max_number_of_vehicles = (road_interval*number_of_lanes) / vehicle_length
average_number_of_vehicles = max_number_of_vehicles * 0.5

# Часові константи
number_of_time_stamps = 100
time_step = 2.0 #(с)
time_stamps = gen.generate_time_stamps(number_of_time_stamps, time_step)

# Константи швидкості
mean_speed = conv.km_per_h_to_m_per_sec(55.0) #(км/год)
speed_deviation = conv.km_per_h_to_m_per_sec(10.0) #(км/год)

# Константи густини
max_density = phys.max_density(number_of_lanes, vehicle_length)
tabled_density_values = gen.generate_tabled_density_values(max_density)
