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
from math import sqrt
from math import exp
from math import pi

from scipy.integrate import quad
from scipy.stats import chi2

#
# Функція для формування гістограми
#

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
  intervals = np.zeros((__calculate_number_of_intervals(min, max, step), 2))
  intervals = __calculate_histogram_intervals(intervals, min, step)
  centers_of_intervals = __calculate_centers_of_intervals(intervals)

  quantities_of_velocities_per_interval = __calculate_number_of_velocties_per_interval(sorted_velocity_values, intervals)
  frequencies = __calculate_frequencies(quantities_of_velocities_per_interval, size)
  densities = __calculate_densities_for_histogram(frequencies, step)

  return (centers_of_intervals, quantities_of_velocities_per_interval, densities)

def __calculate_number_of_intervals(min, max, step) :
  """ Підраховуємо ксть інтервалів на діаграмі """
  number_of_intervals = 0
  current_position = min

  while current_position < max :
    current_position += step
    number_of_intervals += 1

  return number_of_intervals

def __calculate_histogram_intervals(intervals, min, step) :
  """ Обчислюємо значення інтервалів для побудови гістограми """
  calculated_intervals = intervals
  current_position = min

  for i in range(0, calculated_intervals.shape[0]) :
    calculated_intervals[i, 0] = current_position
    current_position += step
    calculated_intervals[i, 1] = current_position

  return calculated_intervals

def __calculate_centers_of_intervals(intervals) :
  """ Обчислюємо центри інтервалів """
  centers_of_intervals = np.zeros(intervals.shape[0])

  for i in range(0, centers_of_intervals.size) :
    shift = (intervals[i][1] - intervals[i][0]) / 2
    centers_of_intervals[i] = intervals[i][0] + shift

  return centers_of_intervals

def __calculate_number_of_velocties_per_interval(sorted_velocity_values, intervals) :
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

def __calculate_frequencies(quantities_of_velocities_per_interval, size) :
  """" Обчислюємо відносні частоти """
  frequencies = np.zeros(quantities_of_velocities_per_interval.size)

  for i in range(0, frequencies.size) :
    frequencies[i] = quantities_of_velocities_per_interval[i] / size

  return frequencies

def __calculate_densities_for_histogram(frequencies, step) :
  """" Обчислюємо щільності """
  densities = np.zeros(frequencies.size)

  for i in range(0, densities.size) :
    densities[i] = frequencies[i] / step

  return densities

#
# Функція для перевірки гіпотез
#

def calculate_mean(centers_of_intervals, quantities_of_velocities_per_interval, size) :
  """ Обчислює середнє значення """
  mean = 0

  for i in range(0, centers_of_intervals.size) :
    mean += centers_of_intervals[i] * quantities_of_velocities_per_interval[i]

  mean /= size
  return mean

def calculate_variance(centers_of_intervals, quantities_of_velocities_per_interval, size, mean) :
  """" Обчислює дисперсію """
  variance = 0

  for i in range(0, centers_of_intervals.size) :
    normalized_value = centers_of_intervals[i] - mean
    variance += (normalized_value*normalized_value) * quantities_of_velocities_per_interval[i]

  variance /= (size - 1)
  return variance

def calculate_deviation(variance) :
  """ Обчислює середнє квадратичне відхилення """
  return sqrt(variance)

def calculate_density_values(centers_of_intervals, mean, deviation) :
  """ Обчислюємо значення функції щільності """
  density_values = np.zeros(centers_of_intervals.size)

  t_values = __calculate_t_values_for_density(centers_of_intervals, mean, deviation)
  phi_values = __calculate_phi_values_for_density(t_values)
  
  for i in range(0, density_values.size) :
    density_values[i] = phi_values[i] / deviation

  return density_values

def __calculate_t_values_for_density(centers_of_intervals, mean, deviation) :
  """ Обчислюємо значення т ітих """
  t_values = np.zeros(centers_of_intervals.size)

  for i in range(0, t_values.size) :
    t_values[i] = (centers_of_intervals[i] - mean) / deviation

  return t_values

def __calculate_phi_values_for_density(t_values) :
  """ Обчислюємо значення фі """
  phi_values = np.zeros(t_values.size)
  divisor = sqrt(2 * pi)

  for i in range(0, phi_values.size) :
    phi_values[i] = __normalized_gaussian_function(t_values[i]) / divisor

  return phi_values

def __normalized_gaussian_function(x) :
  """ Обчислюємо значення функції exp(-(x*x) / 2) """
  return exp(-(x*x) / 2)

def calculate_probability_values(centers_of_intervals, mean, deviation) :
  """ Обчислює ймовірності на всіх інтервалах """
  interval_probabilities = np.zeros(centers_of_intervals.size)
  half_step = (centers_of_intervals[1] - centers_of_intervals[0]) / 2

  for i in range(0, interval_probabilities.size) :
    interval_probabilities[i] = __calculate_probability(
        mean, deviation, 
        centers_of_intervals[i] - half_step, centers_of_intervals[i] + half_step
      )

  return interval_probabilities

def __calculate_probability(mean, deviation, lower_bound, upper_bound) :
  """ Обчислює значення інтегральної функції ймовірності на заданому інтервалі """
  probability = 0
  first_value = (upper_bound - mean) / deviation
  second_value = (lower_bound - mean) / deviation

  probability = __integral_normalized_gaussian_function(first_value) - __integral_normalized_gaussian_function(second_value)

  return probability

def __integral_normalized_gaussian_function(x) :
  """ Обчислює значення інтегральної функцій Гаусса """
  value = 0
  divisor = sqrt(2 * pi)

  (integral_value, _) = quad(__normalized_gaussian_function, 0, x)
  value = integral_value / divisor

  return value

def calculate_cumulative_probability_function(interval_probabilities) :
  """ Обчислює значення інтегральної функції ймовірності """
  return np.add.accumulate(interval_probabilities)

def is_normal_by_pearson(frequencies, interval_probabilities, size, significance_level, number_of_paramaters) :
  """ Визначає чи розподіл є нормальним за критерієм Пірсона """
  calculated_chi_value = 0
  critical_chi_value = 0

  theoretical_frequencies = np.array(interval_probabilities * size, dtype=int)
  for i in range(0, theoretical_frequencies.size) :
    if frequencies[i] < 0.15*frequencies.max() :
      theoretical_frequencies[i] = frequencies[i]
    if theoretical_frequencies[i] == 0 :
      theoretical_frequencies[i] = 1
  if theoretical_frequencies.sum() < frequencies.sum() :
    theoretical_frequencies[int(theoretical_frequencies.size / 2)] += frequencies.sum() - theoretical_frequencies.sum()
  
  numerator = (frequencies - theoretical_frequencies) ** 2
  calculated_chi_value = (numerator / theoretical_frequencies).sum()
  calculated_chi_value = ((frequencies*frequencies) / theoretical_frequencies).sum() - size
  
  degrees_of_freedom = frequencies.size - number_of_paramaters - 1
  critical_chi_value = chi2.isf(significance_level, degrees_of_freedom)

  return (critical_chi_value > calculated_chi_value, calculated_chi_value, critical_chi_value)

def get_confidence_interval(mean, variance, size, alpha=0.95) :
  lower_bound, upper_bound = 0, 0

  deviation_of_estimation = sqrt(variance/size)
  function_value = alpha/2

  t = 0
  current_value = __integral_normalized_gaussian_function(t)
  while (current_value > function_value - 0.0001 and current_value < function_value + 0.0001) == False :
    t += 0.0001
    current_value = __integral_normalized_gaussian_function(t)
  t = float("%.2f" % t)

  estimation = (t*sqrt(variance))/(sqrt(size))
  lower_bound, upper_bound = mean - estimation, mean + estimation

  return ((lower_bound, upper_bound), deviation_of_estimation)
