import numpy as np
from service import time_service
from ortools.constraint_solver import routing_enums_pb2 as pb2
from ortools.constraint_solver import pywrapcp
from utilities.constant import Const
from shapely.geometry import Polygon
from shapely.strtree import STRtree


def validate_input(num_loc, distances, durations, working_limit, search_time,
                   num_vehicles):
    """
    Validate the inputs.
    :param num_loc: number of locations
    :param distances: 2D list present the distances between locations
    :param durations: 2D list present the durations to move between locations
    :param working_limit: working limit (time, distance) of a vehicle
    :param search_time: limit time for searching a solution
    :param num_vehicles: number of vehicle
    :return: error if any
    """
    if num_loc < 2:
        return 'Must have depot and at least 1 more location'
    if not (num_loc == len(distances) == len(durations)):
        return 'Length of locations, distances and durations must be same'
    for d in distances:
        if len(d) != num_loc:
            return 'Length of all distances must be same and equal locations'
        if any(type(num) is not int or num < 0 for num in d):
            return 'All distances must be int and not smaller than 0'
    for d in durations:
        if len(d) != num_loc:
            return 'Length of all durations must be same and equal locations'
        if any(type(num) is not int or num < 0 for num in d):
            return 'All durations must be int and not smaller than 0'
    if (type(working_limit) is not int or working_limit < 1
            or type(search_time) is not int or search_time < 1
            or type(num_vehicles) is not int or num_vehicles < 1):
        return ('Working limit (time or distance), search time and number of '
                'vehicles must be int and greater than 0')
    return ''


def create_routing_model(num_loc, num_vehicles, depot_index):
    """
    Create routing manager and model.
    :param num_loc: number of locations
    :param num_vehicles: number of vehicles
    :param depot_index: index of depot in locations list
    :return: routing manager and model
    """
    manager = pywrapcp.RoutingIndexManager(num_loc, num_vehicles, depot_index)
    routing = pywrapcp.RoutingModel(manager)
    return manager, routing


def register_transit_callback(routing, manager, matrix):
    """
    Create and register a transit callback.
    :param routing: routing model
    :param manager: routing index manager
    :param matrix: distance or time matrix
    :return: transit callback
    """

    def callback(from_index, to_index):
        # Convert from routing variable Index to matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return matrix[from_node][to_node]

    return routing.RegisterTransitCallback(callback)


def build_search_parameters(search_time):
    """
    Setting search parameters.
    :param search_time: limit time for searching a solution
    :return: search parameters
    """
    sp = pywrapcp.DefaultRoutingSearchParameters()
    sp.local_search_metaheuristic = pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    sp.time_limit.seconds = search_time
    sp.log_search = True
    return sp


def check_solution(solution, status):
    """
    Check our optimization solution to see if it is successes.
    :param solution: solution of route optimize process
    :param status: status of routing model
    :return: Error if any
    """
    # If solution not found
    if status == 0:
        return Const.ROUTING_STATUS_0
    if status == 3:
        return Const.ROUTING_STATUS_3
    if status == 4:
        return Const.ROUTING_STATUS_4
    if status == 5:
        return Const.ROUTING_STATUS_5
    if status == 6:
        return Const.ROUTING_STATUS_6
    if not solution:
        return Const.ROUTING_NO_SOLUTION
    return ''


def optimize_route(locations, distances, durations, working_distance=200000,
                   search_time=3, num_vehicles=1):
    """
    Calculate best route from depot (first location) to other locations and
    return back to depot.
    :param locations: list of location name or ID with first location is depot
    :param distances: 2D list present the distances between locations
    :param durations: 2D list present the durations to move between locations
    :param working_distance: maximum moving distance of a vehicle (default 200,000 m)
    :param search_time: limit time for searching a solution (default 3s)
    :param num_vehicles: number of vehicle in this route
    :return: optimized route
    """
    num_loc = len(locations)
    input_error = validate_input(num_loc, distances, durations, working_distance,
                                 search_time, num_vehicles)
    if input_error:
        return {'code': 400, 'message': input_error, 'data': []}
    # Create the routing index manager, routing model
    manager, routing = create_routing_model(num_loc, num_vehicles, num_loc - 1)
    # Create and register a transit callback.
    transit_callback_index = register_transit_callback(routing, manager, distances)
    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # Add Distance constraint
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        working_distance,  # vehicle maximum travel distance
        True,  # start cumulative to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    # This parameter use for balance between routes (in case multiple vehicles)
    distance_dimension.SetGlobalSpanCostCoefficient(5000)
    # Setting guided local search and other parameters
    search_parameters = build_search_parameters(search_time)
    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)
    # If solution not found
    check_error = check_solution(solution, routing.status())
    if check_error:
        return {'code': 200, 'message': check_error, 'data': []}
    # else get our result
    result = []
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route = []
        cur_dis = []
        total_dis = 0
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            cur_dis.append(
                routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            )
            total_dis += cur_dis[-1]
        route.append(manager.IndexToNode(index))
        # Calculate other fields
        cur_dur = []
        total_dur = 0
        for i in range(len(route) - 1):
            cur_dur.append(durations[route[i]][route[i + 1]])
            total_dur += durations[route[i]][route[i + 1]]
            # Get ID into route instead of index
            route[i] = locations[route[i]]
        route[-1] = locations[route[-1]]
        result.append({
            'route': route,
            'distances': cur_dis,
            'durations': cur_dur,
            'total_distance': total_dis,
            'total_duration': total_dur
        })
    return {'code': 200, 'message': 'Success', 'data': result}


def sale_route(locations, time_windows, distances, durations, start_time='08:30',
               lunch_start='12:00', lunch_break=60, waiting_time=5,
               visit_duration=10, working_time=720, search_time=3,
               num_vehicles=1):
    """
    Calculate best route from depot (first location) to other locations (within
    their time window) and return back to depot.
    :param locations: list of location name or ID with first location is depot
    :param time_windows: list of time windows for each location
    :param distances: 2D list present the distances between locations
    :param durations: 2D list present the durations to move between locations
    :param start_time: start time in second, default 8:30. Work begin at 8:00
        and start after 30 minutes of meeting and/or preparing goods.
    :param lunch_start: time for lunch, default 12:00.
    :param lunch_break: time duration for lunch, default 1 hour (60')
    :param waiting_time: allow waiting time in a location, default 5 minutes
    :param visit_duration: time spend in a location, default 10 minutes
    :param working_time: maximum working time of a vehicle (default 12 hours - 720')
    :param search_time: limit time for searching a solution (default 3s)
    :param num_vehicles: number of vehicle in this route
    :return: optimized route
    """
    num_loc = len(locations)
    input_error = validate_input(num_loc, distances, durations, working_time,
                                 search_time, num_vehicles)
    if input_error:
        return {'code': 400, 'message': input_error, 'data': []}
    if num_loc != len(time_windows) + 1:
        mes = 'Must have time windows for all locations except depot'
        return {'code': 400, 'message': mes, 'data': []}
    if (type(lunch_break) is not int or lunch_break < 1
            or type(waiting_time) is not int or waiting_time < 1
            or type(visit_duration) is not int or visit_duration < 1):
        mes = ('Lunch break, waiting time and visit duration must be int and '
               'greater than 0')
        return {'code': 400, 'message': mes, 'data': []}
    depot_index = num_loc - 1
    # Get time configuration
    s_t_minute = time_service.time_to_minute(start_time)
    if 'error' in s_t_minute:
        return {'code': 400, 'message': s_t_minute['error'], 'data': []}
    start_time_m = s_t_minute['minutes']
    l_s_minute = time_service.time_to_minute(lunch_start)
    if 'error' in l_s_minute:
        return {'code': 400, 'message': l_s_minute['error'], 'data': []}
    lunch_start_m = l_s_minute['minutes'] - start_time_m
    lunch_end_m = lunch_start_m + lunch_break
    l_e_str = time_service.minute_to_time(lunch_end_m + start_time_m)
    if 'error' in l_e_str:
        return {'code': 400, 'message': l_e_str['error'], 'data': []}
    lunch_end = l_e_str['time']
    # Get time window for each location
    tw = time_service.convert_time_window(
        time_windows, start_time, start_time_m, lunch_start, lunch_start_m,
        lunch_end, lunch_end_m, locations, working_time
    )
    if 'error' in tw:
        return {'code': 400, 'message': tw['error'], 'data': []}
    tw = tw['time_windows']
    # Add visit duration to durations matrix except from depot (last row)
    np_matrix = np.array(durations)
    np_matrix[:-1, :] += visit_duration
    time_matrix = np_matrix.tolist()
    # Optimize this route
    # Create the routing index manager, routing model
    manager, routing = create_routing_model(num_loc, num_vehicles, depot_index)
    # Create and register a transit callback
    transit_callback_index = register_transit_callback(routing, manager, time_matrix)
    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # Add Time Windows constraint
    time = "Time"
    routing.AddDimension(
        transit_callback_index,
        waiting_time,  # allow waiting time
        working_time,  # maximum time per vehicle
        True,  # Start cumulative to zero.
        time
    )
    # Don't force start cumulative to zero just useful when we have time window
    # for depot like [0, 30] instead of [0, 0]
    time_dimension = routing.GetDimensionOrDie(time)
    # This parameter use for balance between routes (in case multiple vehicles)
    time_dimension.SetGlobalSpanCostCoefficient(500)
    # Add time window constraints for each location except depot
    for location_idx, time_window in enumerate(tw):
        if location_idx == depot_index:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node (depot)
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            tw[depot_index][0], tw[depot_index][1]
        )
    # Instantiate route start and end times to produce feasible times
    for i in range(num_vehicles):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i))
        )
    # Setting parameters
    search_parameters = build_search_parameters(search_time)
    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)
    # If solution not found
    check_error = check_solution(solution, routing.status())
    if check_error:
        return {'code': 200, 'message': check_error, 'data': []}
    # else get our result
    result = []
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route = []
        visit_times = []
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            route.append(manager.IndexToNode(index))
            visit_times.append([solution.Min(time_var), solution.Max(time_var)])
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        route.append(manager.IndexToNode(index))
        visit_times.append([solution.Min(time_var), solution.Max(time_var)])
        # Calculate other fields
        cur_dis = [distances[route[0]][route[1]]]
        total_dis = distances[route[0]][route[1]]
        # Add moving duration from depot to first location
        cur_dur = [time_matrix[route[0]][route[1]]]
        total_dur = time_matrix[route[0]][route[1]]
        # Get ID into route instead of index
        route[0] = locations[route[0]]
        for i in range(1, len(route) - 1):
            cur_dis.append(
                distances[route[i]][route[i + 1]]
            )
            total_dis += distances[route[i]][route[i + 1]]
            # Minus out visit duration from moving duration, and add to visit time
            # end
            temp = time_matrix[route[i]][route[i + 1]] - visit_duration
            cur_dur.append(temp)
            total_dur += temp
            visit_times[i][1] += visit_duration
            # Get ID into route instead of index
            route[i] = locations[route[i]]
        route[-1] = locations[route[-1]]
        # Change visit time from minutes to datetime
        visit_times[0] = [start_time, start_time]
        for i in range(1, len(route)):
            from_time = visit_times[i][0]
            to_time = visit_times[i][1]
            # Add lunchtime
            if from_time >= lunch_start_m:
                from_time += lunch_break
            if to_time > lunch_start_m:
                to_time += lunch_break
            # Change visit time from minutes to datetime
            arr = time_service.minute_to_time(from_time + start_time_m)
            dep = time_service.minute_to_time(to_time + start_time_m)
            if 'error' in arr or 'error' in dep:
                return {
                    'code': 200,
                    'message': 'Visit time after midnight',
                    'data': []
                }
            visit_times[i] = [arr['time'], dep['time']]
        result.append({
            'route': route,
            'visit_times': visit_times,
            'lunch_time': [lunch_start, lunch_end],
            'distances': cur_dis,
            'durations': cur_dur,
            'total_distance': total_dis,
            'total_duration': total_dur
        })
    return {'code': 200, 'message': 'Success', 'data': result}


def check_overlap(names, routes):
    """
    Check for overlapping routes.
    :param names: list of names or IDs of routes
    :param routes: coordinates (lat, long) in each route
    :return: overlap routes if any
    """
    if len(routes) != len(names):
        mes = 'Difference length between routes and names'
        return {'code': 400, 'message': mes, 'data': []}
    elif len(routes) > 100 or len(routes[0]) > 100:
        mes = 'Only support up to 100 routes and 100 locations per route'
        return {'code': 400, 'message': mes, 'data': []}
    polygons = []
    # For each route
    for i in range(len(routes)):
        # Polygon needs at least 3 coordinates
        if len(routes[i]) < 3:
            mes = f'{names[i]}: has less than 3 locations'
            return {'code': 400, 'message': mes, 'data': []}
        # Validate coordinates
        try:
            arr = np.array(routes[i], dtype=np.float64)
        except (ValueError, TypeError):
            mes = f'{names[i]}: all coordinates must be float'
            return {'code': 400, 'message': mes, 'data': []}
        if arr.ndim != 2 or arr.shape[1] != 2:
            mes = f'{names[i]}: coordinates must be pairs [lat, long]'
            return {'code': 400, 'message': mes, 'data': []}
        # Get route information and polygon (just need it's convex hull)
        polygon = Polygon(routes[i]).convex_hull
        polygons.append(polygon)
    # Use STRtree to avoid O(n^2) loop
    tree = STRtree(polygons)
    result = []
    # Check for overlap
    for i in range(len(polygons)):
        for other in tree.query(polygons[i]):
            # Avoid itself and duplicates
            j = int(other)
            if j <= i:
                continue
            # Get the names of overlapping routes
            if polygons[i].intersects(polygons[j]):
                result.append((names[i], names[j]))
    return {'code': 200, 'message': 'Success', 'data': result}
