# Helper class to construct and retrieve individual parts of an request endpoint
# and the json data associated with it
class EndpointRequest():
    def __init__(self, proto, hostname, port, path, json_data):
        self.proto = proto
        self.hostname = hostname
        self.port = port
        self.path = path
        self.json_data = json_data
    
    def proto(self):
        return self.proto
    
    def hostname(self):
        return self.hostname

    def port(self):
        return self.port

    def path(self):
        return self.path
    
    def json_data(self):
        return self.json_data

    def endpoint(self):
        return self.proto + "://" + self.hostname + ":" + self.port + "/" + self.path

def build_http_endpoint_req(host, port, path, json_data):
    return EndpointRequest('http', host, port, path, json_data)