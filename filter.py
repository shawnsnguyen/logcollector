class LogFilter():
    # note that the incl/excl keywords are *OR* filters (meaning matching any of the supplied keyword)
    # adding an *AND* filter would need another set of parameters if we need to support that
    def __init__(self, incl_keywords=None, excl_keywords=None):
        self.incl_keywords = incl_keywords.split(',') if incl_keywords else None
        # ensure log line *doesnt contain any* excluded keywords
        self.excl_keywords = excl_keywords.split(',') if excl_keywords else None

    # return true if log line matches an incl keyword 
    # and doesnt contain any excl keywords, else false
    # if no include/exclude keywords were specified, skip check.
    def filter(self, log_line):
        match = True
        if self.incl_keywords:
            match &= any(True if incl_keyword in log_line else False for incl_keyword in self.incl_keywords)
        if self.excl_keywords:
            match &= all(False if excl_keyword in log_line else True for excl_keyword in self.excl_keywords)
        return match

# static builder utility to construct log filter from the request's json data
def build_log_filter(req_json_data):
    # filters for include/exclude keywords
    incl_filter = req_json_data.get('include_keywords')
    excl_filter = req_json_data.get('exclude_keywords')
    log_filter = LogFilter(incl_filter, excl_filter)
    return log_filter