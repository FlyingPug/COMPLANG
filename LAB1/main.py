import json
import urllib
from datetime import datetime
from wsgiref.simple_server import make_server

import pytz


def get_time_in_timezone(timezone_name):
    try:
        timezone = pytz.timezone(timezone_name) if timezone_name else pytz.UTC
        return datetime.now(timezone)
    except pytz.UnknownTimeZoneError:
        return None


def app(environ, start_response):
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', 'GET')
    response_body = ''
    status = '200 OK'
    content_type = 'text/html'

    if method == 'GET':
        if path == '/':
            current_time = get_time_in_timezone(None)
            response_body = f"<html><body><h1>Current Server Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}</h1></body></html>"
        else:
            tz_name = path[1:]
            current_time = get_time_in_timezone(tz_name)
            if current_time:
                response_body = f"<html><body><h1>Current Time in {tz_name}: {current_time.strftime('%Y-%m-%d %H:%M:%S')}</h1></body></html>"
            else:
                status = '404 Not Found'
                response_body = "<html><body><h1>Timezone not found</h1></body></html>"
    elif method == 'POST':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)

        if path == '/api/v1/time':
            tz_name = params.get('tz')[0]
            current_time = get_time_in_timezone(tz_name)
            response_body = json.dumps({"time": current_time.isoformat()})
            content_type = 'application/json'
        elif path == '/api/v1/date':
            tz_name = params.get('tz')[0]
            current_time = get_time_in_timezone(tz_name)
            response_body = json.dumps({"date": current_time.date().isoformat()})
            content_type = 'application/json'
        elif path == '/api/v1/datediff':
            start_date = params.get('start')[0]
            end_date = params.get('end')[0]

            tz = params.get('tz')[0]

            start_dt = datetime.strptime(start_date, '%m.%d.%Y %H:%M:%S')
            end_dt = datetime.strptime(end_date, '%m.%d.%Y %H:%M:%S')

            if tz:
                start_dt = pytz.timezone(tz).localize(start_dt)
                end_dt = pytz.timezone(tz).localize(end_dt)

            delta = end_dt - start_dt
            response_body = json.dumps({"difference": str(delta)})
            content_type = 'application/json'
        else:
            status = '404 Not Found'
            response_body = json.dumps({"error": "Not Found"})

    headers = [('Content-type',  content_type),
               ('Content-Length', str(len(response_body)))]
    start_response(status, headers)
    return [response_body.encode('utf-8')]


with make_server('', 8000, app) as httpd:
    print("Listening on port 8000...")
    httpd.serve_forever()
