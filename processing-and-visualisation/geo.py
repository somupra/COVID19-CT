from geopy.distance import vincenty
import sys

args = sys.argv[1:]

# lat1 = 35.642962
# lon1 = 139.611743

# lat2 = 35.641745
# lon2 = 139.60923

lat1 = args[2]
lon1 = args[0]

lat2 = args[3]
lon2 = args[1]

distance = vincenty((lat1, lon1), (lat2, lon2)).meters

if (distance < 200):
    print(distance)
else:
    print(-1)
