import json
import os
import requests

from concurrent.futures import ThreadPoolExecutor
from constants import MAX_WORKERS
from collector import build_log_collector
from endpoints import build_http_endpoint_req
from flask import Flask, Response, jsonify, request
from util import list_files

app = Flask(__name__)

@app.route('/list', methods = ['GET', 'POST'])
def list():
    files = list_files()
    return jsonify({'log_files': files})

@app.route('/query', methods = ['GET', 'POST'])
def query():
    req_data = request.get_json()

    log_collector = build_log_collector(req_data)
    log_events, err = log_collector.collect()

    if err:
        # todo: define error type responses in separate class
        return Response(err, status=400)
    return jsonify({'logs': log_events})

@app.route('/distributed_query', methods = ['GET', 'POST'])
def distributed_query():
    req_data = request.get_json()
    endpoint_path = 'query'

    socket_addresses_str = req_data.get('socket_addresses')
    if not socket_addresses_str:
        return Response("missing required hosts key in json data", status=400)
    host_port_pairs = [socket_addr.split(':') for socket_addr in socket_addresses_str.split(',')]
    endpoint_reqs = [build_http_endpoint_req(host, port, endpoint_path, req_data) for host, port in host_port_pairs]
    res = {endpoint_req.endpoint(): json_resp for endpoint_req, json_resp in parallel_fetch_urls(endpoint_reqs)}
    return res

# return a tuple containing the original request and fetch result
def fetch(endpoint_request):
    return endpoint_request, requests.post(endpoint_request.endpoint(), json=endpoint_request.json_data)

# perform multiple requests concurrently with a fixed set of threads.
# the more pythonic way to handle this since the bulk of the time is
# spent waiting for network io is to use an async web framework with
# coroutines built in...
def parallel_fetch_urls(endpoint_requests):
    req_resp_pairs = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for result in executor.map(fetch, endpoint_requests):
            req, resp = result
            req_resp_pairs.append((req, resp.json()))
    return req_resp_pairs
