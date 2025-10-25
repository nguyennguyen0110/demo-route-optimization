import joblib


class FrequencyPredictor:
    _model = joblib.load(filename='model/best_model_2025-10-23.joblib')
    require_features = ('order_amount', 'order_count', 'channel', 'class',
                        'branch', 'type', 'state')
    numerical_columns = {'order_amount', 'order_count'}
    valid_data = {
        'channel': {'GT_100', 'GT_200', 'GT_300', 'GT_400', 'others'},
        'class': {'N1', 'N2'},
        'branch': {'10000342', 'MARVAL', 'NPP01', 'others'},
        'type': {'101', '201', '305', '402', 'others'},
        'state': {'43', '79', '80', 'others'}
    }
    one_hot_columns = [
        'channel_GT_100', 'channel_GT_200', 'channel_GT_300', 'channel_GT_400',
        'channel_others', 'class_N1', 'class_N2', 'branch_10000342',
        'branch_MARVAL', 'branch_NPP01', 'branch_others', 'type_101',
        'type_201', 'type_305', 'type_402', 'type_others', 'state_43',
        'state_79', 'state_80', 'state_others'
    ]
    all_columns = [
        'order_amount', 'order_count', 'channel_GT_100', 'channel_GT_200',
        'channel_GT_300', 'channel_GT_400', 'channel_others', 'class_N1',
        'class_N2', 'branch_10000342', 'branch_MARVAL', 'branch_NPP01',
        'branch_others', 'type_101', 'type_201', 'type_305', 'type_402',
        'type_others', 'state_43', 'state_79', 'state_80', 'state_others'
    ]

    @classmethod
    def suggest(cls, customer):
        """
        Suggest visit frequency of input customer.
        :param customer: information of customer
        :return: sale frequency suggest for customer
        """
        return cls._model.predict(customer)
