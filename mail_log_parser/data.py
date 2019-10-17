from collections import defaultdict


# {<ID>: {'client_email': <''>, 'receivers': { <receiver_email>: <0/1> } }
QUEUE_TRACKER = defaultdict(lambda: {'client_email': '', 'receivers': {}})

# {<client_email>: <num_of_letters_sent>}
EMAIL_TRACKER = {}

DELIVERY_TRACKER = {'delivered': 0, 'undelivered': 0}