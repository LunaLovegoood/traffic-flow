import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

import convertor as conv

def plot_velocity_distribution(plane_velocities) :
  """ Рисує графік розподілу швидкості транспорту """
  # Підписуємо графік
  plt.figure("Розподіл швидкості")
  plt.title("Розподіл швидкості")
  plt.xlabel(r'Швидкість $v$ (км/год)')
  plt.ylabel(r'Ймовірність швидкості $p$')

  # Отримуємо значення для побудови графіку розподілу швидкості
  (velocity_probabilities, bins) = np.histogram(conv.plane_velocities_to_km_per_h(plane_velocities), bins=25, density=True)
  velocity_values = np.array(0.5*(bins[1:]+bins[:-1]))

  # Отримуємо значення для побудови інтерпольованого графіку розподілу швидкості
  tabled_velocity_values = np.linspace(0, velocity_values.max(), 1000)
  spliner = make_interp_spline(velocity_values, velocity_probabilities)
  interpolated_velocity_probabilities = spliner(tabled_velocity_values)

  plt.plot(tabled_velocity_values, interpolated_velocity_probabilities, color='#ffc214') # Будуємо інтерпольований графік розподілу швидкості
  plt.hist(conv.plane_velocities_to_km_per_h(plane_velocities), 
      bins=50, density=True, color='c', histtype='bar', ec='black') # Будуємо гістограму значень швидкості

def plot_fundamental_diagram(tabled_density_values, deduced_flow_rates, mean_densities, mean_flow_rates) :
  """ Рисує фундаментальну діаграму транспортних потоків """
  # Підписуємо графік
  plt.figure("Фундаментальна діаграма транспортних потоків")
  plt.title("Фундаментальна діаграма транспортних потоків")
  plt.xlabel(r'Густина $\rho$ (ксть авто/25м)')
  plt.ylabel(r'Потік $f$ (авто/с)')

  plt.plot(tabled_density_values, deduced_flow_rates, color='b') # Будуємо фундаментальну діаграму
  plt.scatter(mean_densities, mean_flow_rates, color='g', s=3.5*3.5) # Наносимо на графік фактичні значення потоку в залежності від густини

  max_flow_rate_value = deduced_flow_rates.max() # Знаходимо максимальне значення потоку
  max_flow_rate_density = tabled_density_values[np.where(deduced_flow_rates == max_flow_rate_value)][0] # Знаходимо відповідне йому значення густини

  plt.ylim(0, max_flow_rate_value + 0.6) # Змінюємо межі значень f для коректного відображення на графіку
  plt.annotate( # Підписуємо максимальне значення f на графіку
      s=r'max $f$', 
      xy=(max_flow_rate_density - 0.044, max_flow_rate_value + 0.1)
    )

def show_plots() :
  """ Відображає графіки побудовані графіки"""
  plt.show()