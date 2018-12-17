import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

import convertor as conv

def plot_fundamental_diagram() :
  pass

def plot_velocity_distribution(plane_velocities) :
  (y, bins) = np.histogram(conv.plane_velocities_to_km_per_h(plane_velocities), bins=50, density=True)
  x = np.array(0.5*(bins[1:]+bins[:-1]))

  x_smooth = np.linspace(0, x.max(), 1000)
  spl = make_interp_spline(x, y)
  y_interp = spl(x_smooth)

  plt.figure("Velocity distribution")
  plt.plot(x_smooth, y_interp, color='r')
  plt.hist(conv.plane_velocities_to_km_per_h(plane_velocities), bins=50, density=True, color='b')

def show_plots() :
  plt.show()