from flask import Flask, request, render_template, json
from service import route_service, frequency_service, cluster_service
from route.api import api_bp
from utilities.constant import Const

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

_data = {
    'loc': ['A', 'B', 'C', 'D', 'E', 'Depot'],
    'du_n': ['dur_a', 'dur_b', 'dur_c', 'dur_d', 'dur_e', 'dur_depot'],
    'du_v': [
        [0, 45, 67, 90, 106, 80],
        [47, 0, 27, 49, 70, 29],
        [66, 29, 0, 32, 55, 29],
        [84, 51, 33, 0, 33, 35],
        [101, 73, 54, 33, 0, 60],
        [74, 32, 29, 38, 62, 0]
    ],
    'di_n': ['dis_a', 'dis_b', 'dis_c', 'dis_d', 'dis_e', 'dis_depot'],
    'di_v': [
        [0, 18300, 30300, 46600, 77500, 37800],
        [19500, 0, 12000, 28300, 43800, 17900],
        [30700, 16500, 0, 17700, 33200, 13400],
        [45400, 31300, 18200, 0, 21300, 16900],
        [72500, 46800, 33800, 21400, 0, 32500],
        [34400, 20200, 13100, 17600, 33000, 0]
    ]
}


@app.route('/', methods=['GET'])
def root():
    # Render demo page
    return render_template('index.html')


@app.route('/optimize-route', methods=['GET', 'POST'])
def optimize_route():
    template = 'optimize_route.html'
    if request.method == 'GET':
        return render_template(template, output={}, raw_in='', raw_out='', d=_data)
    # Else POST method
    if request.content_type != Const.FORM:
        res = {'code': 400, 'message': Const.NOT_FORM, 'data': []}
        return render_template(template, output=res, raw_in='',
                               raw_out=json.dumps(res, indent=4), d=_data)
    info = request.form
    params = {'locations': info.getlist('locations')}
    dis_a = info.getlist(key='dis_a', type=int)
    dis_b = info.getlist(key='dis_b', type=int)
    dis_c = info.getlist(key='dis_c', type=int)
    dis_d = info.getlist(key='dis_d', type=int)
    dis_e = info.getlist(key='dis_e', type=int)
    dis_depot = info.getlist(key='dis_depot', type=int)
    params['distances'] = [dis_a, dis_b, dis_c, dis_d, dis_e, dis_depot]
    dur_a = info.getlist(key='dur_a', type=int)
    dur_b = info.getlist(key='dur_b', type=int)
    dur_c = info.getlist(key='dur_c', type=int)
    dur_d = info.getlist(key='dur_d', type=int)
    dur_e = info.getlist(key='dur_e', type=int)
    dur_depot = info.getlist(key='dur_depot', type=int)
    params['durations'] = [dur_a, dur_b, dur_c, dur_d, dur_e, dur_depot]
    if 'optional' in info:
        optional = ['working_time', 'search_time', 'num_vehicles']
        for k in optional:
            if k in info:
                params[k] = int(info[k]) if info[k].isdigit() else info[k]
    raw_input = _inline_list(json.dumps(params, indent=4))
    if len(params['locations']) > 15:
        mes = 'Just support up to 15 locations (include depot) in this demo'
        result = {'code': 400, 'message': mes, 'data': []}
    else:
        result = route_service.optimize_route(**params)
    raw_output = _inline_list(json.dumps(result, indent=4))
    return render_template(template, output=result, raw_in=raw_input,
                           raw_out=raw_output, d=_data)


@app.route('/sale-route', methods=['GET', 'POST'])
def sale_route():
    template = 'sale_route.html'
    if request.method == 'GET':
        return render_template(template, output={}, raw_in='', raw_out='', d=_data)
    # Else POST method
    if request.content_type != Const.FORM:
        res = {'code': 400, 'message': Const.NOT_FORM, 'data': []}
        return render_template(template, output=res, raw_in='',
                               raw_out=json.dumps(res, indent=4), d=_data)
    info = request.form
    params = {'locations': info.getlist('locations'), 'time_windows': []}
    from_time = info.getlist('from_time')
    to_time = info.getlist('to_time')
    for f, t in zip(from_time, to_time):
        if f and t:
            params['time_windows'].append([f, t])
        else:
            params['time_windows'].append([])
    dis_a = info.getlist(key='dis_a', type=int)
    dis_b = info.getlist(key='dis_b', type=int)
    dis_c = info.getlist(key='dis_c', type=int)
    dis_d = info.getlist(key='dis_d', type=int)
    dis_e = info.getlist(key='dis_e', type=int)
    dis_depot = info.getlist(key='dis_depot', type=int)
    params['distances'] = [dis_a, dis_b, dis_c, dis_d, dis_e, dis_depot]
    dur_a = info.getlist(key='dur_a', type=int)
    dur_b = info.getlist(key='dur_b', type=int)
    dur_c = info.getlist(key='dur_c', type=int)
    dur_d = info.getlist(key='dur_d', type=int)
    dur_e = info.getlist(key='dur_e', type=int)
    dur_depot = info.getlist(key='dur_depot', type=int)
    params['durations'] = [dur_a, dur_b, dur_c, dur_d, dur_e, dur_depot]
    if 'optional' in info:
        if 'start_time' in info:
            params['start_time'] = info['start_time']
        if 'lunch_start' in info:
            params['lunch_start'] = info['lunch_start']
        optional = [
            'lunch_break', 'waiting_time', 'visit_duration', 'working_time',
            'search_time', 'num_vehicles'
        ]
        for k in optional:
            if k in info:
                params[k] = int(info[k]) if info[k].isdigit() else info[k]
    raw_input = _inline_list(json.dumps(params, indent=4))
    if len(params['locations']) > 15:
        mes = 'Just support up to 15 locations (include depot) in this demo'
        result = {'code': 400, 'message': mes, 'data': []}
    else:
        result = route_service.sale_route(**params)
    raw_output = _inline_list(json.dumps(result, indent=4))
    return render_template(template, output=result, raw_in=raw_input,
                           raw_out=raw_output, d=_data)


@app.route('/check-overlap', methods=['GET', 'POST'])
def check_overlap():
    template = 'check_overlap.html'
    demo = {
        'names': ['Route 1', 'Route 2', 'Route 3'],
        'routes': [
            [
                [10.82373766402676, 106.65712309789507],
                [10.770518006608803, 106.64313322416673],
                [10.779070000427357, 106.7621314384404],
                [10.836376739721254, 106.77549460012666]
            ],
            [
                [10.7967331801708, 106.7221612851624],
                [10.813767972757294, 106.8531317754408],
                [10.869729481655309, 106.80313018669835]
            ],
            [
                [10.981562194491769, 106.88038432220381],
                [10.917887559437533, 106.93723627476294],
                [10.980749413312065, 106.99960783268875],
                [10.931978445003686, 107.14035781232542]
            ]
        ],
        'variables': [
            ['route_1_lat', 'route_1_long'],
            ['route_2_lat', 'route_2_long'],
            ['route_3_lat', 'route_3_long']
        ]
    }
    if request.method == 'GET':
        return render_template(template, output={}, raw_in='', raw_out='', d=demo)
    # Else POST method
    if request.content_type != Const.FORM:
        res = {'code': 400, 'message': Const.NOT_FORM, 'data': []}
        return render_template(template, output=res, raw_in='',
                               raw_out=json.dumps(res, indent=4), d=demo)
    info = {'names': request.form.getlist('names')}
    route_1_lat = request.form.getlist('route_1_lat')
    route_1_long = request.form.getlist('route_1_long')
    route_2_lat = request.form.getlist('route_2_lat')
    route_2_long = request.form.getlist('route_2_long')
    route_3_lat = request.form.getlist('route_3_lat')
    route_3_long = request.form.getlist('route_3_long')
    try:
        route_1 = [
            (float(lat), float(long))
            for lat, long in zip(route_1_lat, route_1_long)
        ]
        route_2 = [
            (float(lat), float(long))
            for lat, long in zip(route_2_lat, route_2_long)
        ]
        route_3 = [
            (float(lat), float(long))
            for lat, long in zip(route_3_lat, route_3_long)
        ]
        info['routes'] = [route_1, route_2, route_3]
        res = route_service.check_overlap(info['names'], info['routes'])
    except (ValueError, TypeError):
        res = {'code': 400, 'message': 'Lat-Long must be float', 'data': []}
    raw_input = _inline_list(json.dumps(info, indent=4))
    raw_output = _inline_list(json.dumps(res, indent=4))
    return render_template(template, output=res, raw_in=raw_input,
                           raw_out=raw_output, d=demo)


@app.route('/suggest-frequency', methods=['GET', 'POST'])
def suggest_frequency():
    template = 'suggest_frequency.html'
    if request.method == 'GET':
        return render_template(template, output={}, raw_in='', raw_out='')
    # Else POST method
    if request.content_type != Const.FORM:
        res = {'code': 400, 'message': Const.NOT_FORM, 'data': []}
        return render_template(template, output=res, raw_in='',
                               raw_out=json.dumps(res, indent=4))
    data = request.form.to_dict()
    try:
        data['order_amount'] = float(data['order_amount'])
        data['order_count'] = float(data['order_count'])
    except (ValueError, TypeError, KeyError):
        pass  # frequency_service.suggest_frequency will handle this
    raw_input = _inline_list(json.dumps(data, indent=4))
    res = frequency_service.suggest_frequency(data)
    raw_output = _inline_list(json.dumps(res, indent=4))
    return render_template(template, output=res, raw_in=raw_input,
                           raw_out=raw_output)


@app.route('/cluster-customer', methods=['GET', 'POST'])
def cluster_customer():
    template = 'cluster_customer.html'
    demo = [
        [10.82373766402676, 106.65712309789507],
        [10.770518006608803, 106.64313322416673],
        [10.779070000427357, 106.7621314384404],
        [10.836376739721254, 106.77549460012666],
        [10.7967331801708, 106.7221612851624],
        [10.813767972757294, 106.8531317754408],
        [10.869729481655309, 106.80313018669835],
        [10.981562194491769, 106.88038432220381],
        [10.917887559437533, 106.93723627476294],
        [10.980749413312065, 106.99960783268875],
        [10.931978445003686, 107.14035781232542]
    ]
    if request.method == 'GET':
        return render_template(template, output={}, raw_in='', raw_out='', d=demo)
    # Else POST method
    if request.content_type != Const.FORM:
        res = {'code': 400, 'message': Const.NOT_FORM, 'data': []}
        return render_template(template, output=res, raw_in='',
                               raw_out=json.dumps(res, indent=4), d=demo)
    if 'groups' not in request.form:
        res = {'code': 400, 'message': 'Missing groups', 'data': []}
        return render_template(template, output=res, raw_in='',
                               raw_out=json.dumps(res, indent=4), d=demo)
    latitude = request.form.getlist('latitude')
    longitude = request.form.getlist('longitude')
    try:
        coordinates = [
            (float(lat), float(long)) for lat, long in zip(latitude, longitude)
        ]
    except (ValueError, TypeError):
        coordinates = [(lat, long) for lat, long in zip(latitude, longitude)]
    try:
        groups = int(request.form['groups'])
    except (ValueError, TypeError):
        groups = request.form['groups']
    info = {'coordinates': coordinates, 'groups': groups}
    raw_input = _inline_list(json.dumps(info, indent=4))
    res = cluster_service.cluster_by_position(coordinates, groups)
    raw_output = _inline_list(json.dumps(res, indent=4))
    return render_template(template, output=res, raw_in=raw_input,
                           raw_out=raw_output, d=demo)


def _inline_list(string):
    """
    From json string turn all the last level lists into one line.
    :param string: string with json format
    :return: string with inline list.
    """
    res = ''
    last_index = 0
    start = -1
    for i in range(len(string)):
        if string[i] == '[':
            start = i
        if string[i] == ']' and start >= last_index:
            inline = [line.strip() for line in string[start:i].split('\n')]
            for j in range(1, len(inline) - 2):
                inline[j] += ' '
            res += string[last_index:start] + ''.join(inline)
            last_index = i
    res += string[last_index:]
    return res


if __name__ == '__main__':
    app.run()
