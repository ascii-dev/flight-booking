def return_value(status, message, data=None, status_code=200):
    return_object = dict()
    return_object['status'] = status
    return_object['message'] = message
    if data:
        return_object['data'] = data

    return return_object, status_code
