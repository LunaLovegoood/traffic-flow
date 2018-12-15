import numpy as np

def km_per_h_to_m_per_sec(speed) :
    """Converts km/h to m/s"""
    return speed * (1000 / 3600)

def m_per_sec_to_km_per_h(speed) :
    """Converts m/s to km/h"""
    return speed * 3.6

def km_to_m(distance) :
    """Converts km to m"""
    return distance * 1000

def m_to_km(distance) :
    """Converts m to km"""
    return distance / 1000

def h_to_s(time) :
    """Converts hours to seconds"""
    return time / 3600

def s_to_h(time) :
    """Converts seconds to hours"""
    return time * 3600

def plane_velocities_to_km_per_h(plane_velocities) :
    converted_velocities = np.zeros(plane_velocities.size)

    for i in range(0, plane_velocities.size) :
        converted_velocities[i] = m_per_sec_to_km_per_h(plane_velocities[i])

    return converted_velocities

