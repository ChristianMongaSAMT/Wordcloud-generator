# event.py

from collections import defaultdict

eventi = defaultdict(list)

def subscribe(event_type, fn):
    eventi[event_type].append(fn)

def post_event(event_type, data): 
    if event_type in eventi:
        for fn in eventi[event_type]:
            fn(data)