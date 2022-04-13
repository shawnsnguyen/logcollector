# Defaults used for log query web app. These defaults should ideally be configurable by param during server startup..

# Dir to allow clients to request for logs under
LOG_DIR = '/var/log/'

# Num log entries to return per log request if no limit is specified
LOG_EVENT_COLLECT_COUNT = 20

# Max number of workers/threads for spawning parallel http requests
MAX_WORKERS = 5
