'''

'''

import googlemaps
from datetime import datetime

key = ''
gmaps = googlemaps.Client(key=key)

position = gmaps.geocode('DHGTVT')
reverse_geocode = gmaps.reverse_geocode(position)

now = datetime.now()

direction = gmaps.directions("hanoi", "noibai", mode="transit", departure_time=)


