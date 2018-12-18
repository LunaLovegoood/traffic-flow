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

def print_basic_constants(road_interval, number_of_lanes, number_of_vehicles, number_of_time_stamps) :
  """ Виведення базових константних величин моделі """
  print('Базові константи: ')
  print('Величина інтервалу дороги: ', conv.m_to_km(road_interval), ' (км)')
  print('Кількість смуг дороги: ', number_of_lanes)
  print('Кількість автомобілів: ', number_of_vehicles)
  print('Кількість часових відліків: ', number_of_time_stamps, end='\n\n')

def print_max_values(max_velocity, max_density, max_flow_rate) :
  """ Виведення максимальних значень величин моделі """
  print('Максимальні значення:')
  print('Максимальне значення швидкості max(v) = ', conv.m_per_sec_to_km_per_h(max_velocity), ' (км/год)')
  print('Максимальне значення густини max(густини) = ', max_density, ' (ксть авто/25м)')
  print('Максимальне значення потоку max(f) = ', max_flow_rate, ' (авто/с)', end='\n\n')

def print_mean_values(mean_velocity, mean_density, mean_flow_rate) :
  """ Виведення середніх значень величин моделі """
  print('Середні значення:')
  print('Середнє значення швидкості <v> = ', conv.m_per_sec_to_km_per_h(mean_velocity), ' (км/год)')
  print('Середнє значення густини <густина> = ', mean_density, ' (ксть авто/25м)')
  print('Середнє значення потоку <f> = ', mean_flow_rate, ' (авто/с)', end='\n\n')
