from astroquery.jplhorizons import Horizons
from astropy.time import Time
import datetime

now = datetime.datetime.now()

JD = Time(now).jd
print(JD)
"""
string_date = f"{now:%Y-%m-%d %H:%M:%S}"
print(string_date)

Y = now.year  . . . . 

 
. . . .day_frac = (H + (m / 60) + (s / 3600)) / 24

A = int(Y/100)
B = int(A/4)
C = 2 - A + B

E = int(365.25*(Y+4716))
#print(E)
F = int(30.6001*(M+1))
JD = (C + (D + day_frac) + E + F - 1524.5)

#jd => datetime
#convert date time to julian day
#using formula and
#print(jd) where var => jd
"""
alma_coords = {'lon': -67.7536, 'lat': -23.0292, 'elevation': 5.076}

obj = Horizons(
    id='ceres',
    location=alma_coords,
    epochs=JD,
    id_type='smallbody'
)

efem = obj.ephemerides()
print(efem)
Horizons.clear_cache()
