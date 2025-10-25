import pandas as pd
from utilities.model import FrequencyPredictor as Predictor


def suggest_frequency(info):
    """
    Suggest sale frequency for a customer.
    :param info: information of customer
    :return: visit frequency suggested for customer
    """
    # Check for require features
    data = {}
    for c in Predictor.require_features:
        if c not in info:
            return {'code': 400, 'message': f'{c} is missing', 'data': ''}
        # Check type of numerical columns
        if c in Predictor.numerical_columns:
            if (type(info[c]) is not int) and (type(info[c]) is not float):
                mes = f'{c} must be int or float'
                return {'code': 400, 'message': mes, 'data': ''}
            data[c] = info[c]
        # Check for valid categorical value
        else:
            value = info[c] if type(info[c]) is str else str(info[c])
            if value not in Predictor.valid_data[c]:
                mes = f'{c} cannot take value {value}'
                return {'code': 400, 'message': mes, 'data': ''}
            # One-hot encode
            data[f'{c}_{value}'] = 1
    # One-hot encode - fill other columns
    for c in Predictor.one_hot_columns:
        if c not in data:
            data[c] = 0
    # Get into dataframe
    df = pd.DataFrame(data, index=[0])
    # Make sure our columns in right order and needed only
    df = df[Predictor.all_columns]
    frequency = Predictor.suggest(df)
    return {'code': 200, 'message': f'Success', 'data': frequency[0]}
