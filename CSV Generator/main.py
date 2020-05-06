import json
import datetime
import csv
from geopy.distance import geodesic

def create_entry(coordinates, start_time, end_time, id, final_data):
    for entry in coordinates:
        final_data.append([id, entry[0][0], entry[0][1], start_time, end_time, entry[1]/100])
        print("Added Entry: ", id, entry[0][0], entry[0][1], start_time, end_time, entry[1]/100)


def export_final_data(paths, extrapolate=False, extrapolation_interval_in_secs=None):
    final_data = []
    for entry in paths:
        json_path = entry[0]
        id = entry[1]
        with open(json_path) as data:
            json_data = json.load(data)
            
            for loc_dict in json_data['timelineObjects']:
                if 'placeVisit' in loc_dict.keys():
                    static_dict = loc_dict['placeVisit']
                    start_time = int(static_dict['duration']['startTimestampMs'])
                    end_time = int(static_dict['duration']['endTimestampMs'])
                    coordinates = []

                    # coordinates have tuples like ((lat, long), confidence)
                    # confidence for central point is 1
                    # confidence for other points is confidence/100
                    if 'centerLatE7' in static_dict.keys():
                        coordinates.append(((static_dict['centerLatE7']/1e7, static_dict['centerLngE7']/1e7), 100))
                    loc = static_dict['location']
                    
                    if 'latitudeE7' in loc.keys():
                        coordinates.append(
                            ((loc['latitudeE7']/1e7, loc['longitudeE7']/1e7), loc['locationConfidence'])
                        )
                    if 'otherCandidateLocations' in static_dict.keys():
                        for other_loc_dict in static_dict['otherCandidateLocations']:
                            coordinates.append(
                                ((other_loc_dict['latitudeE7']/1e7, other_loc_dict['longitudeE7']/1e7), other_loc_dict['locationConfidence'])
                            )
                    # now create the entry for these coordinates
                    create_entry(coordinates, start_time, end_time, id, final_data)

                    # some json files have childVisits too, check it and process
                    # maybe write a similar function with same logic as above

                    if 'childVisits' in static_dict.keys():
                        for dict in static_dict['childVisits']:
                            child_start_time = int(dict['duration']['startTimestampMs'])
                            child_end_time = int(dict['duration']['endTimestampMs'])

                            child_coordinates = []
                            if 'centerLatE7' in dict.keys():
                                child_coordinates.append(((dict['centerLatE7']/1e7, dict['centerLngE7']/1e7), 100))

                            loc = dict['location']
                            child_coordinates.append(
                                ((loc['latitudeE7']/1e7, loc['longitudeE7']/1e7), loc['locationConfidence'])
                            )
                            if 'otherCandidateLocations' in dict.keys():
                                for child_other_loc_dict in static_dict['otherCandidateLocations']:
                                    child_coordinates.append(
                                        ((child_other_loc_dict['latitudeE7']/1e7, child_other_loc_dict['longitudeE7']/1e7), child_other_loc_dict['locationConfidence'])
                                    )
                            create_entry(child_coordinates, child_start_time, child_end_time, id, final_data)

                    # we now have the data for one static location point. start_time, end_time are for which this is recorded
                    # coordinates are with their confidences, there is also a central coordinate with confidence 1
                    # process this as individual coordinates for this specific duration (start_time, end_time being the same for all)
                    
                elif 'activitySegment' in loc_dict.keys():
                    dynamic_dict = loc_dict['activitySegment']
                    dynamic_start_time = int(dynamic_dict['duration']['startTimestampMs'])
                    dynamic_end_time = int(dynamic_dict['duration']['endTimestampMs'])
                    path = []

                    # path have the same format except that they have confidence as -1
                    path.append(
                        ((dynamic_dict['startLocation']['latitudeE7']/1e7, dynamic_dict['startLocation']['longitudeE7']/1e7), -100)
                    )
                    if 'waypointPath' in dynamic_dict.keys():
                        for waypoint in dynamic_dict['waypointPath']['waypoints']:
                            if 'latE7' in waypoint.keys():
                                path.append(
                                    ((waypoint['latE7']/1e7, waypoint['lngE7']/1e7), -100)
                                )
                            else:
                                path.append(
                                    ((waypoint['latitudeE7']/1e7, waypoint['longitudeE7']/1e7), -100)
                                )
                    
                    path.append(
                        ((dynamic_dict['endLocation']['latitudeE7']/1e7, dynamic_dict['endLocation']['longitudeE7']/1e7), -100)
                    )
                    
                    # extrapolate the data if flag is passed -- we do this by connecting paths from startpoint to endpoints 
                    # and interval for which the extrapolation needs to be done
                    if extrapolate:
                        path_len = path_length(path)
                        journey_time = (dynamic_end_time - dynamic_start_time)/1000
                        speed = path_len / journey_time
                        
                        new_points = []
                        for i in range(len(path)-1):
                            interval_dist = speed * extrapolation_interval_in_secs
                            start = path[i][0]
                            end = path[i+1][0]
                            segmented = False
                            
                            print("segment", i+1)
                            while not segmented:
                                # segment the interval between path[i] and path[i+1]
                                # print((start[1], start[0]), (end[1], end[0]))
                                dist = geodesic((start[1], start[0]), (end[1], end[0])).meters

                                if dist: 
                                    param_t = interval_dist / dist
                                    # we define a parameter t which will define the equation of the line since the scales of distances 
                                    # are not equal -- meaning geodesic and (d1**2 + d2**2)**0.5 won't give results
                                    # and latitude and longitude might overflow
                                else:
                                    segmented = True
                                    continue
                                
                                if param_t < 1 and param_t > 0:
                                    gen_lat = (1 - param_t)*start[0] + param_t*end[0]
                                    gen_long = (1 - param_t)*start[1] + param_t*end[1]
                                    
                                    print(gen_lat, gen_long)
                                    new_points.append(
                                        ((gen_lat, gen_long), -100)
                                    )
                                    start = (gen_lat, gen_long)
                                    continue
                                else:
                                    segmented = True
                                    continue
                        path += new_points

                    create_entry(path, dynamic_start_time, dynamic_end_time, id, final_data)

    return final_data

def path_length(path):
    path_len = 0
    for i in range(len(path) - 1):
        # print((path[i][0][1], path[i][0][0]), (path[i+1][0][1], path[i+1][0][0]))
        path_len += geodesic((path[i][0][1], path[i][0][0]), (path[i+1][0][1], path[i+1][0][0])).meters

    return path_len
        

paths = [
    ('test_monthly.json', 'guddu'),
    ('test_monthly2.json', 'prof_swaprava'),
    ('test_monthly3.json', 'prof_hamim')
]

################## DRIVER CALL #######################
# paths is necessary, extrapolate = False will cause no extrapolation and path segmentation, extrapolation_interval_in_secs is the 
# intervals between segments, for setting 0.6 seconds, a data of 10^5 order is the output

final_data = export_final_data(paths, extrapolate=True, extrapolation_interval_in_secs=60)

with open("results_static_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(final_data)