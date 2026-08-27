from astropy.coordinates import SkyCoord
from astroplan import FixedTarget
from astroplan import Observer

coordinates = SkyCoord('19h50m47.6s','+08d52m12.0s', frame='icrs')
altair = FixedTarget(name='Altair', coord=coordinates)

print(altair)

observer = Observer.at_site('alma')

print(observer)

objetivo = FixedTarget.from_name("M87")

print(objetivo)
