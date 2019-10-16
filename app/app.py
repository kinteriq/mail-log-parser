def read_log_line(filepath):
    with open(filepath, 'r') as log:
        while True:
            line = log.readline()
            if not line:
                return
            yield line