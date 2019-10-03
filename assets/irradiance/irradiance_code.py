import numpy as np
from datetime import datetime

# Solar Constant
SOLAR_CONSTANT = 1361

# Earth-Sun-Distance
DAYS_IN_YEAR = 365.265
PERIHELION_DAY = 3
SEMI_MAJOR_AXIS = 1.496e11+10
ECCENTRICITY = 0.0167
AU = 149597870700
R_SUN = 6.957e+8

def days_from_perihelion(day_of_year):
    '''Returns number of days from January 3rd based on day_of_year input.'''
    n = abs(day_of_year - PERIHELION_DAY)
    return (DAYS_IN_YEAR - n) if n > (DAYS_IN_YEAR/2) else n

def angle_from_perihelion(day_of_year):
    '''Returns angle from perihelion day based on day_of_year input.'''
    days_from_p = days_from_perihelion(day_of_year)
    return (2*np.pi*days_from_p)/DAYS_IN_YEAR

def earth_sun_distance_kepler(day_of_year):
    '''Returns Earth-Sun distance using Keplerian approximation.'''
    angle_from_p = angle_from_perihelion(day_of_year)
    return SEMI_MAJOR_AXIS*(1 - ECCENTRICITY**2)/(1 + ECCENTRICITY*np.cos(angle_from_p))

def earth_sun_distance_ratio(day_of_year):
    '''Return the square of the mean Earth-Sun distance to current Earth-Sun distance ratio.'''
    return ((R_SUN + AU) / earth_sun_distance_kepler(day_of_year))**2

# Solar Zenith Angle
def declination(day):
    '''Return the declination angle of a given day.'''
    return np.radians(23.45)*np.sin(np.radians((360/365)*(day+284)))

def hour_angle(hour, longitude):
    '''Return the hour angle of a given hour.'''
    hour += longitude/15
    hour = hour - 12 if hour >= 12 else 12 - hour
    return np.radians(hour*15)

def cos_of_solar_zenith(day, hour, latitude, longitude):
    '''Return the cosine of the solar zenith angle at a given day, hour, and latitude.'''
    dec = declination(day)
    hra = hour_angle(hour, longitude)
    lat = np.radians(latitude)
    return (np.sin(lat)*np.sin(dec) + np.cos(lat)*np.cos(dec)*np.cos(hra))

# Transmittance
def transmittance(cloud_cover=0, offset=75):
    '''Returns transmittance ratio between 0 and 1, with default offset = 75 and default cloud cover = 0.'''
    return ((100 - cloud_cover) / 100) * (offset/100)

# Flux Density
def flux_density(date, latitude, longitude):
    '''Returns solar flux density in watts/m^2 based on day, hour, latitude, and optional atmospheric loss.'''
    day_of_year = (date - datetime(date.year, 1, 1)).days
    cos_sz = cos_of_solar_zenith(day_of_year, date.hour, latitude, longitude)
    if cos_sz < 0:  # cos_sz is negative then the sun is below the horizon.
        return 0
    distance_factor = earth_sun_distance_ratio(day_of_year)
    return SOLAR_CONSTANT*distance_factor*cos_sz*(transmittance())