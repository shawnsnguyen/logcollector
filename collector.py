from cmath import log
import os

class Collector():
    def __init__(self, log_dir, log_file, limit, log_filter):
        self.log_path = os.path.join(log_dir, log_file)
        self.log_filter = log_filter
        self.limit = limit

    # Collect entries from the tail-end of the log file until we reach
    # the limit specified after optionally filtering. Reading and adjusting
    # the pointer starting from tail-end can be much more efficient than reading
    # the entire file from beginning, especially if the log files are large.
    def collect(self):
        processed_lines = []
        tail_offset = self.limit + 1

        if not os.path.isfile(self.log_path):
            return (None, "invalid log file")

        with open(self.log_path, 'rb') as fd:
            while len(processed_lines) <= self.limit:
                try:
                    # try seeking by position amount of offset from end of file
                    fd.seek(-tail_offset, os.SEEK_END)
                except IOError:
                    # Potentially ran out of entries to seek to
                    fd.seek(0)
                    break
                finally:
                    log_lines = fd.readlines()
                    processed_lines = self.process(log_lines)
                tail_offset *= 2 
        # Return entries in reversed order assuming that logs were originally
        # sorted in ascending timestamp order.
        # Since we seek by multiplying position by 2 each loop, we may have extra
        # log entries. In such case, trim any excess up to 'limit' amount.
        return (processed_lines[-self.limit::][::-1], None)

    # perform any post processing logic on raw log lines collected here
    def process(self, log_lines):
        # decode utf8 text and strip trailing new line
        cur_lines = [line.decode('utf-8').strip() for line in log_lines]
        processed_lines = [line for line in cur_lines if self.log_filter.filter(line)]
        return processed_lines