import joblib


class FrequencyPredictor:
    _model = joblib.load(filename='/model/best_model.joblib')
    map_features = {
        'order_amount': 'OrdAmt', 'order_count': 'OrderCount',
        'channel_GT_100': 'Channel_GT_100', 'channel_GT_200': 'Channel_GT_200',
        'channel_GT_300': 'Channel_GT_300', 'channel_GT_400': 'Channel_GT_400',
        'channel_KA_700': 'Channel_KA_700', 'channel_Others': 'Channel_Others',
        'class_id_N1': 'ClassId_N1', 'class_id_N2': 'ClassId_N2',
        'territory_BTB': 'Territory_BTB', 'territory_DBSCL': 'Territory_DBSCL',
        'territory_DNB': 'Territory_DNB', 'territory_HCM': 'Territory_HCM',
        'territory_TB': 'Territory_TB', 'branch_id_10000342': 'BranchID_10000342',
        'branch_id_MARVAL': 'BranchID_MARVAL', 'branch_id_Others': 'BranchID_Others',
        'shop_type_101': 'ShopType_101', 'shop_type_102': 'ShopType_102',
        'shop_type_201': 'ShopType_201', 'shop_type_305': 'ShopType_305',
        'shop_type_402': 'ShopType_402', 'shop_type_Others': 'ShopType_Others',
        'state_43': 'State_43', 'state_79': 'State_79', 'state_80': 'State_80',
        'state_Others': 'State_Others'
    }
    require_features = ('order_amount', 'order_count', 'channel', 'class_id',
                        'territory', 'branch_id', 'shop_type', 'state')
    numerical_columns = {'order_amount', 'order_count'}
    valid_data = {
        'channel': {'GT_100', 'GT_200', 'GT_300', 'GT_400', 'KA_700', 'Others'},
        'class_id': {'N1', 'N2'},
        'territory': {'BTB', 'DBSCL', 'DNB', 'HCM', 'TB'},
        'branch_id': {'10000342', 'MARVAL', 'Others'},
        'shop_type': {'101', '102', '201', '305', '402', 'Others'},
        'state': {'43', '79', '80', 'Others'},
    }
    one_hot_columns = [
        'channel_GT_100', 'channel_GT_200', 'channel_GT_300', 'channel_GT_400',
        'channel_KA_700', 'channel_Others', 'class_id_N1', 'class_id_N2',
        'territory_BTB', 'territory_DBSCL', 'territory_DNB', 'territory_HCM',
        'territory_TB', 'branch_id_10000342', 'branch_id_MARVAL',
        'branch_id_Others', 'shop_type_101', 'shop_type_102', 'shop_type_201',
        'shop_type_305', 'shop_type_402', 'shop_type_Others', 'state_43',
        'state_79', 'state_80', 'state_Others'
    ]
    all_columns = [
        'order_amount', 'order_count', 'channel_GT_100', 'channel_GT_200',
        'channel_GT_300', 'channel_GT_400', 'channel_KA_700', 'channel_Others',
        'class_id_N1', 'class_id_N2', 'territory_BTB', 'territory_DBSCL',
        'territory_DNB', 'territory_HCM', 'territory_TB', 'branch_id_10000342',
        'branch_id_MARVAL', 'branch_id_Others', 'shop_type_101', 'shop_type_102',
        'shop_type_201', 'shop_type_305', 'shop_type_402', 'shop_type_Others',
        'state_43', 'state_79', 'state_80', 'state_Others'
    ]

    @classmethod
    def suggest(cls, customer):
        """
        Suggest visit frequency of input customer.
        :param customer: information of customer
        :return: sale frequency suggest for customer
        """
        return cls._model.predict(customer)
