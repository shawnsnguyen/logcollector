import os

from flask import Flask, Response, jsonify, request
from filter import LogFilter
from util import list_files
from collector import Collector
from constants import LOG_DIR, DEFAULT_LOG_EVENT_COLLECT_COUNT

app = Flask(__name__)

@app.route('/list', methods = ['GET', 'POST'])
def list():
    files = list_files(LOG_DIR)
    return jsonify({'log_files': files})

@app.route('/query', methods = ['GET', 'POST'])
def query():
    req_data = request.get_json()

    # specific log to retrieve
    log_name = req_data.get('log_name')

    # max number of log entries from end of log file
    event_limit = int(req_data.get('event_limit') or DEFAULT_LOG_EVENT_COLLECT_COUNT)

    # filters for include/exclude keywords
    incl_filter = req_data.get('include_keywords')
    excl_filter = req_data.get('exclude_keywords')
    log_filter = LogFilter(incl_filter, excl_filter)

    # collector to aggregate and process logs
    log_collector = Collector(LOG_DIR, log_name, event_limit, log_filter)
    log_events, err_string = log_collector.collect()

    if err_string:
        # todo: define error type responses in separate class
        return Response(err_string, status=400)
    return jsonify({'logs': log_events})