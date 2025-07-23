class Const:
    # REST request content_type & response mimetype, content_type, parameters
    JSON = 'application/json'
    RES_PARAM = {'status': 200, 'mimetype': JSON, 'content_type': JSON}
    NOT_JSON = 'Content type must be application/json'
    FORM = 'application/x-www-form-urlencoded'
    NOT_FORM = 'Content type must be application/x-www-form-urlencoded'

    # OR Tools routing status
    ROUTING_STATUS_0 = 'Problem not solved yet'
    ROUTING_STATUS_3 = 'Solution not found'
    ROUTING_STATUS_4 = 'Time limit reached'
    ROUTING_STATUS_5 = 'Model, model parameters, or flags are not valid'
    ROUTING_STATUS_6 = 'Problem proven to be infeasible'
    ROUTING_NO_SOLUTION = 'Cannot solve this route with current time config'
