from datetime import datetime as dt


VALID_FLIGHT_DATA = {
    'from': 'Lagos, Nigeria',
    'to': 'San Francisco, California, USA',
    'departure': dt.now().strftime("%Y-%m-%d %H:%M:%S"),
    'arrival': dt.now().strftime("%Y-%m-%d %H:%M:%S"),
}

INVALID_FLIGHT_DATA = {
    'from': '',
    'to': '',
    'departure': '',
    'arrival': '',
}
