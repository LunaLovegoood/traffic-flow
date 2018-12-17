import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

import convertor as conv

def plot_velocity_distribution(plane_velocities) :
  """ Рисує графік розподілу швидкості транспорту """
  plt.figure("Розподіл швидкості")
  plt.xlabel(r'Швидкість $v$ (км/год)')
  plt.ylabel(r'Ймовірність швидкості $p$')

  # Отримуємо значення для побудови графіку розподілу швидкості
  (velocity_probabilities, bins) = np.histogram(conv.plane_velocities_to_km_per_h(plane_velocities), bins=50, density=True)
  velocity_values = np.array(0.5*(bins[1:]+bins[:-1]))

  # Отримуємо значення для побудови інтерпольованого графіку розподілу швидкості
  tabled_velocity_values = np.linspace(0, velocity_values.max(), 1000)
  spliner = make_interp_spline(velocity_values, velocity_probabilities)
  interpolated_velocity_probabilities = spliner(tabled_velocity_values)

  plt.plot(tabled_velocity_values, interpolated_velocity_probabilities, color='r') # Будуємо інтерпольований графік розподілу швидкості
  plt.hist(conv.plane_velocities_to_km_per_h(plane_velocities), bins=50, density=True, color='b') # Будуємо гістограму значень швидкості

def plot_fundamental_diagram(tabled_density_values, deduced_flow_rates, mean_densities, mean_flow_rates) :
  """ Рисує фундаментальну діаграму транспортних потоків """
  plt.figure("Фундаментальна діаграма транспортних потоків")
  plt.xlabel(r'Густина $\rho$ (авто/100м)')
  plt.ylabel(r'Потік $f$ (авто/с)')

  plt.plot(tabled_density_values, deduced_flow_rates, color='b') # Будуємо фундаментальну діаграму
  plt.scatter(mean_densities, mean_flow_rates, color='g', s=3.5*3.5) # Наносимо на графік фактичні значення потоку в залежності від густини

def show_plots() :
  """ Відображає графіки побудовані графіки"""
  plt.show()