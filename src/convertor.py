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

def km_per_h_to_m_per_sec(speed) :
  """ Переводить (км/год) в (м/с) """
  return speed * (1000 / 3600)

def m_per_sec_to_km_per_h(speed) :
  """ Переводить (м/с) в (км/год) """
  return speed * 3.6

def km_to_m(distance) :
  """ Переводить (км) в (м) """
  return distance * 1000

def m_to_km(distance) :
  """ Переводить (м) в (км) """
  return distance / 1000

def h_to_s(time) :
  """ Переводить (год) в (с) """
  return time / 3600

def s_to_h(time) :
  """ Переводить (с) в (год) """
  return time * 3600

def plane_velocities_to_km_per_h(plane_velocities) :
  """ Переводить масив швидкостей з (м/с) в (км/год) """
  converted_velocities = np.zeros(plane_velocities.size)

  for i in range(0, plane_velocities.size) :
    converted_velocities[i] = m_per_sec_to_km_per_h(plane_velocities[i])

  return converted_velocities

