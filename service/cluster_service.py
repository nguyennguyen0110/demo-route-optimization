import numpy as np
from sklearn.cluster import KMeans


def cluster_by_position(coordinates, groups):
    """
    Cluster locations into k group by their positions (lat-long).
    :param coordinates: list of location's positions (lat-long)
    :param groups: number of groups want to cluster
    :return: array of labels correspond to locations.
    """
    if len(coordinates) > 200:
        mes = 'Support up to 200 locations only'
        return {'code': 400, 'message': mes, 'data': []}
    if type(groups) is not int or groups > len(coordinates):
        mes = 'groups must be int and not greater and number of locations'
        return {'code': 400, 'message': mes, 'data': []}
    try:
        arr = np.array(coordinates, dtype=np.float64)
    except (ValueError, TypeError):
        mes = 'coordinates must be float and in pairs [lat, long]'
        return {'code': 400, 'message': mes, 'data': []}
    if arr.ndim != 2 or arr.shape[1] != 2:
        mes = 'coordinates must be pairs [lat, long]'
        return {'code': 400, 'message': mes, 'data': []}
    kmeans = KMeans(n_clusters=groups)
    kmeans.fit(arr)
    return {'code': 200, 'message': 'Success', 'data': kmeans.labels_.tolist()}
