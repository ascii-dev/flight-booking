def return_value(status, message, data, status_code=200):
    return {
        "status": status,
        "message": message,
        "data": data,
    }, status_code
