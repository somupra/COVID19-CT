import json
import datetime
import csv
from geopy.distance import geodesic

def create_entry(coordinates, start_time, end_time, id, final_data):
    for entry in coordinates:
        final_data.append([id, entry[0][0]/1e7, entry[0][1]/1e7, start_time, end_time, entry[1]])
        print("Added Entry: ", id, entry[0][0]/1e7, entry[0][1]/1e7, start_time, end_time, entry[1])


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
                        coordinates.append(((static_dict['centerLatE7'], static_dict['centerLngE7']), 1))
                    loc = static_dict['location']
                    
                    if 'latitudeE7' in loc.keys():
                        coordinates.append(
                            ((loc['latitudeE7'], loc['longitudeE7']), loc['locationConfidence'])
                        )
                    if 'otherCandidateLocations' in static_dict.keys():
                        for other_loc_dict in static_dict['otherCandidateLocations']:
                            coordinates.append(
                                ((other_loc_dict['latitudeE7'], other_loc_dict['longitudeE7']), other_loc_dict['locationConfidence'])
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
                                child_coordinates.append(((dict['centerLatE7'], dict['centerLngE7']), 1))

                            loc = dict['location']
                            child_coordinates.append(
                                ((loc['latitudeE7'], loc['longitudeE7']), loc['locationConfidence'])
                            )
                            if 'otherCandidateLocations' in dict.keys():
                                for child_other_loc_dict in static_dict['otherCandidateLocations']:
                                    child_coordinates.append(
                                        ((child_other_loc_dict['latitudeE7'], child_other_loc_dict['longitudeE7']), child_other_loc_dict['locationConfidence'])
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
                        ((dynamic_dict['startLocation']['latitudeE7'], dynamic_dict['startLocation']['longitudeE7']), -1)
                    )
                    if 'waypointPath' in dynamic_dict.keys():
                        for waypoint in dynamic_dict['waypointPath']['waypoints']:
                            if 'latE7' in waypoint.keys():
                                path.append(
                                    ((waypoint['latE7'], waypoint['lngE7']), -1)
                                )
                            else:
                                path.append(
                                    ((waypoint['latitudeE7'], waypoint['longitudeE7']), -1)
                                )
                    
                    path.append(
                        ((dynamic_dict['endLocation']['latitudeE7'], dynamic_dict['endLocation']['longitudeE7']), -1)
                    )
                    
                    # extrapolate the data if flag is passed -- we do this by connecting paths from startpoint to endpoints 
                    # and interval for which the extrapolation needs to be done
                    # if extrapolate:
                    #     path_len = path_lenght(path)
                    #     journey_time = (dynamic_end_time - dynamic_start_time)/1000
                    #     speed = path_len / journey_time
                        
                    #     for i in range(len(path)-1):
                    #         start = path[i]
                    #         end = path[i+1]
                    #         dist = geodesic((start[0][1], start[0][0]), (end[0][1], end[0][0])).meters

                    #         if dist > speed * extrapolation_interval_in_secs:



                    create_entry(path, dynamic_start_time, dynamic_end_time, id, final_data)

    return final_data

def path_lenght(path):
    path_len = 0
    for i in range(len(path) - 1):
        path_len += geodesic((path[i][0][1], path[i][0][0]), (path[i+1][0][1], path[i+1][0][0])).meters

    return path_len
        

paths = [
    ('test_monthly.json', 'guddu'),
    ('test_monthly2.json', 'prof_swaprava'),
    ('test_monthly3.json', 'prof_hamim')
]

final_data = export_final_data(paths)

with open("results_static_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(final_data)