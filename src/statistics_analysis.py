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

from math import log

def sort_velocity_values(velocities) :
  """ Сортує вибірку зі значень швидкості """
  sorted_velocity_values = np.sort(velocities, axis=None)
  return sorted_velocity_values

def get_min_and_max_velocity_values(velocities) :
  """ Повертає min та max значення швидкості у вигляді кортежу """
  return (velocities.min(), velocities.max())

def calculate_step(min, max, size) :
  """ Обчислюємо крок або довжину інтервалу за формулою Стерджесс """
  return (max - min) / (1 + 3.322*log(size, 10))

def calculate_data_for_histogram(sorted_velocity_values, min, max, step, size) :
  """" Підраховуємо необхідні дані для гістограми """
  intervals = np.zeros((calculate_number_of_intervals(min, max, step), 2))
  intervals = calculate_histogram_intervals(intervals, min, step)
  centers_of_intervals = calculate_centers_of_intervals(intervals)

  quantities_of_velocities_per_interval = calculate_number_of_velocties_per_interval(sorted_velocity_values, intervals)
  frequencies = calculate_frequencies(quantities_of_velocities_per_interval, size)
  densities = calculate_densities_for_histogram(frequencies, step)

  return (centers_of_intervals, densities)

def calculate_number_of_intervals(min, max, step) :
  """ Підраховуємо ксть інтервалів на діаграмі """
  number_of_intervals = 0
  current_position = min

  while current_position < max :
    current_position += step
    number_of_intervals += 1

  return number_of_intervals

def calculate_histogram_intervals(intervals, min, step) :
  """ Обчислюємо значення інтервалів для побудови гістограми """
  calculated_intervals = intervals
  current_position = min

  for i in range(0, calculated_intervals.shape[0]) :
    calculated_intervals[i, 0] = current_position
    current_position += step
    calculated_intervals[i, 1] = current_position

  return calculated_intervals

def calculate_centers_of_intervals(intervals) :
  """ Обчислюємо центри інтервалів """
  centers_of_intervals = np.zeros(intervals.shape[0])

  for i in range(0, centers_of_intervals.size) :
    shift = (intervals[i][1] - intervals[i][0]) / 2
    centers_of_intervals[i] = intervals[i][0] + shift

  return centers_of_intervals

def calculate_number_of_velocties_per_interval(sorted_velocity_values, intervals) :
  """ Обчислюємо ксті швидкостей для кожного інтервалу """
  quantities_of_velocities_per_interval = np.zeros(intervals.shape[0], dtype=int)
  number_of_velocities = 0
  current_velocity_index = 0

  for i in range(0, quantities_of_velocities_per_interval.size) :
    if current_velocity_index >= sorted_velocity_values.size :
      break
    while sorted_velocity_values[current_velocity_index] < intervals[i][1] :
      current_velocity_index +=1
      number_of_velocities += 1
      if current_velocity_index >= sorted_velocity_values.size :
        break
    quantities_of_velocities_per_interval[i] = number_of_velocities
    number_of_velocities = 0

  return quantities_of_velocities_per_interval

def calculate_frequencies(quantities_of_velocities_per_interval, size) :
  """" Обчислюємо відносні частоти """
  frequencies = np.zeros(quantities_of_velocities_per_interval.size)

  for i in range(0, frequencies.size) :
    frequencies[i] = quantities_of_velocities_per_interval[i] / size

  return frequencies

def calculate_densities_for_histogram(frequencies, step) :
  """" Обчислюємо щільності """
  densities = np.zeros(frequencies.size)

  for i in range(0, densities.size) :
    densities[i] = frequencies[i] / step

  return densities
