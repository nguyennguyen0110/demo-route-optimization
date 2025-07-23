from flask import Blueprint, Response, json, request
from utilities.constant import Const
from service import route_service, frequency_service, cluster_service

api_bp = Blueprint('api', __name__)


@api_bp.route(rule='/', methods=['POST'])
def root():
    # Check content_type
    if request.content_type != Const.JSON:
        res = {'code': 400, 'message': Const.NOT_JSON, 'data': []}
    else:
        data = 'Welcome to Route Optimization API demo'
        res = {'code': 200, 'message': 'Success', 'data': data}
    return Response(response=json.dumps(res), **Const.RES_PARAM)


@api_bp.route('/optimize-route', methods=['POST'])
def optimize_route():
    # Check content_type
    if request.content_type != Const.JSON:
        res = {'code': 400, 'message': Const.NOT_JSON, 'data': []}
        return Response(response=json.dumps(res), **Const.RES_PARAM)
    # Get request information
    info = request.get_json()
    if ('locations' not in info
            or 'distances' not in info or 'durations' not in info):
        mes = 'Must have locations, distances, durations information in request'
        res = {'code': 400, 'message': mes, 'data': []}
    elif len(info['locations']) > 15:
        mes = 'Just support up to 15 locations (include depot) in this demo'
        res = {'code': 400, 'message': mes, 'data': []}
    else:
        params = {
            'locations': info['locations'],
            'distances': info['distances'],
            'durations': info['durations']
        }
        # These are optional parameters
        optionals = {'working_time', 'search_time', 'num_vehicles'}
        # Get optional parameters if passed
        for key in optionals:
            if key in info:
                params[key] = info[key]
        # Get result
        res = route_service.optimize_route(**params)
    return Response(response=json.dumps(res), **Const.RES_PARAM)


@api_bp.route('/sale-route', methods=['POST'])
def sale_route():
    # Check content_type
    if request.content_type != Const.JSON:
        res = {'code': 400, 'message': Const.NOT_JSON, 'data': []}
        return Response(response=json.dumps(res), **Const.RES_PARAM)
    # Get request information
    info = request.get_json()
    if ('locations' not in info or 'time_windows' not in info
            or 'distances' not in info or 'durations' not in info):
        mes = 'Missing locations, time_windows, distances or durations'
        res = {'code': 400, 'message': mes, 'data': []}
    elif len(info['locations']) > 15:
        mes = 'Just support up to 15 locations (include depot) in this demo'
        res = {'code': 400, 'message': mes, 'data': []}
    else:
        params = {
            'locations': info['locations'],
            'time_windows': info['time_windows'],
            'distances': info['distances'],
            'durations': info['durations']
        }
        # These are optional parameters
        optionals = {
            'start_time', 'lunch_start', 'lunch_break', 'waiting_time',
            'visit_duration', 'working_time', 'search_time', 'num_vehicles'
        }
        # Get optional parameters if passed
        for key in optionals:
            if key in info:
                params[key] = info[key]
        # Get result
        res = route_service.sale_route(**params)
    return Response(response=json.dumps(res), **Const.RES_PARAM)


@api_bp.route('/check-overlap', methods=['POST'])
def check_overlap():
    # Check content_type
    if request.content_type != Const.JSON:
        res = {'code': 400, 'message': Const.NOT_JSON, 'data': []}
    else:
        # Get request information
        info = request.get_json()
        if 'routes' not in info or 'names' not in info:
            mes = 'Must have names and routes'
            res = {'code': 400, 'message': mes, 'data': []}
        elif len(info['routes']) > 10 or len(info['routes'][0]) > 30:
            mes = 'Demo just support up to 10 routes and 30 locations per route'
            res = {'code': 400, 'message': mes, 'data': []}
        else:
            res = route_service.check_overlap(info['names'], info['routes'])
    return Response(response=json.dumps(res), **Const.RES_PARAM)


@api_bp.route('/suggest-frequency', methods=['POST'])
def suggest_frequency():
    # Check content_type
    if request.content_type != Const.JSON:
        res = {'code': 400, 'message': Const.NOT_JSON, 'data': []}
    else:
        # Get request information
        info = request.get_json()
        res = frequency_service.suggest_frequency(info)
    return Response(response=json.dumps(res), **Const.RES_PARAM)


@api_bp.route('/cluster-customer', methods=['POST'])
def cluster_customer():
    # Check content_type
    if request.content_type != Const.JSON:
        res = {'code': 400, 'message': Const.NOT_JSON, 'data': []}
    else:
        # Get request information
        info = request.get_json()
        if 'coordinates' not in info or 'groups' not in info:
            mes = 'Must have coordinates and groups'
            res = {'code': 400, 'message': mes, 'data': []}
        else:
            res = cluster_service.cluster_by_position(info['coordinates'],
                                                      info['groups'])
    return Response(response=json.dumps(res), **Const.RES_PARAM)
