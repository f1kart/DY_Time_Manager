from datetime import datetime

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return value.strftime(format)
