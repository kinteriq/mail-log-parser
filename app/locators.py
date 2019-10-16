# TODO {ID: from}
OPEN_QUEUE = r'(\S+): from=<(.+)>, size=.+, nrcpt=.+'
# TODO SERVER_NOTICES = {ID: 0/1}
SERVER_NOTICE_QUEUE = r'(\S+): from=<>, size=.+, nrcpt=.+'
# TODO {ID:{from: '', to: {'': 0/1, ...}}}
SEND_ATTEMPT = r'(\S+): to=<(.+)>, relay=.+, dsn=.+, status=(\w+)'
# TODO count status -> del d[ID]
CLOSE_QUEUE = r'(\S+): removed'