def time_to_minute(str_time):
    """
    Convert time in string format hh:mm into minutes.
    :param str_time: time in string format hh:mm
    :return: minutes (h*60 + m)
    """
    time = str_time.split(':')
    if len(time) != 2:
        return {'error': f'{str_time} not follow format hh:mm'}
    try:
        h = int(time[0])
        m = int(time[1])
    except (ValueError, TypeError):
        return {'error': f'hh or mm in hh:mm is not correct'}
    if h > 23:
        return {'error': 'Hour must less than 24'}
    if m > 59:
        return {'error': 'Minute must less than 60'}
    return {'minutes': h * 60 + m}


def minute_to_time(minute):
    """
    Convert minutes into time string format hh:mm
    :param minute: time minutes
    :return: string format hh:mm
    """
    if type(minute) is not int:
        return {'error': f'{minute} is not int'}
    time = [minute // 60]
    if time[0] > 23:
        return {'error': 'Time exceeds 24 hours'}
    minute = minute % 60
    time.append(minute)
    return {'time': ':'.join([f'0{e}' if e < 10 else str(e) for e in time])}


def convert_time_window(time_windows, start_time, start_time_m, lunch_start,
                        lunch_start_m, lunch_end, lunch_end_m, locations,
                        working_time):
    """
    Get time window in seconds after start time from format hh:mm
    :param time_windows: Time windows in string hh:mm
    :param start_time: Start time in string
    :param start_time_m: Start time in minutes
    :param lunch_start: Lunch time in string
    :param lunch_start_m: Lunch time in minutes
    :param lunch_end: Lunch end in string
    :param lunch_end_m: Lunch end in minutes
    :param locations: List of locations with depot at the end
    :param working_time: Maximum working time in minutes
    :return: time window
    """
    data = []
    for i in range(len(time_windows)):
        # If time windows of current location is set and passed
        if len(time_windows[i]) == 2:
            # Change to seconds
            from_time = time_to_minute(time_windows[i][0])
            to_time = time_to_minute(time_windows[i][1])
            if 'error' in from_time:
                return from_time
            if 'error' in to_time:
                return to_time
            from_time = from_time['minutes'] - start_time_m
            to_time = to_time['minutes'] - start_time_m
            # Check for validation
            if (from_time < 0) or (to_time < 0):
                mes = (f'Time window of customer {locations[i]} at index {i} is '
                       f'sooner than start time {start_time}')
                return {'error': mes}
            if from_time >= to_time:
                mes = (f'Time window of customer {locations[i]} at index {i}: '
                       f'from-time must sooner than to-time')
                return {'error': mes}
            if (((from_time >= lunch_start_m) and (from_time < lunch_end_m))
                    or ((to_time > lunch_start_m) and (to_time <= lunch_end_m))):
                mes = (f'Time window of location {locations[i]} at index {i} '
                       f'overlap lunchtime from {lunch_start} to {lunch_end}')
                return {'error': mes}
            # Add to time windows
            data.append([from_time, to_time])
        # If time window not specified for this location
        else:
            # Add default time window
            data.append([0, working_time])
    # Add time window for depot
    data.append([0, 0])
    return {'time_windows': data}
