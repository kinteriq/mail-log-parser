class ManageData:
    def __init__(self, queue_tracker_db, email_tracker_db, delivery_tracker):
        self.queue_tracker_db = queue_tracker_db
        self.email_tracker_db = email_tracker_db
        self.delivery_tracker_db = delivery_tracker

    def manage_queue_tracker(self, fields):
        """
        Receive one of the following located groups as <args>:
            [('ID', <id>), ('client_email', <email>)];
            [('ID', <id>), ('client_email', <''>)];
            [('ID', <id>), ('receivers', <email>), ('status', <status>)];
            [('ID', <id>)];
        and store it in the <queue_tracker_db>.
        """
        if len(fields) == 1:
            ID = fields[0][1]
            self.manage_email_tracker(ID)
            self.manage_delivery_tracker(ID)
            del self.queue_tracker_db[ID]
        elif len(fields) == 2:
            ID, client_email = (f[1] for f in fields)
            self.queue_tracker_db[ID]['client_email'] = client_email
        elif len(fields) == 3:
            ID, receiver, status = (f[1] for f in fields)
            if status == 'sent':
                code = 1
            else:
                code = 0
            self.queue_tracker_db[ID]['receivers'][receiver] = code

    def manage_email_tracker(self, ID):
        """
        Retrieve client's email from the <queue_tracker_db> by <ID>
        with the amount of 'receivers' whose 'status' == 1
        and store it in the <email_tracker_db>.
        """
        client_email = self.queue_tracker_db[ID]['client_email']
        receivers = self.queue_tracker_db[ID]['receivers']
        delivered_mail = [r for r in receivers if receivers[r] == 1]
        if client_email in self.email_tracker_db:
            self.email_tracker_db[client_email] += len(delivered_mail)
        else:
            self.email_tracker_db[client_email] = len(delivered_mail)

    def manage_delivery_tracker(self, ID):
        """
        Go through all receivers of <ID> queue of <queue_tracker_db>,
        and add their delivery statuses to the <delivery_tracker> counter
        """
        receivers = self.queue_tracker_db[ID]['receivers']
        for receiver in receivers:
            if receivers[receiver] == 1:
                self.delivery_tracker_db['delivered'] += 1
            else:
                self.delivery_tracker_db['undelivered'] += 1
