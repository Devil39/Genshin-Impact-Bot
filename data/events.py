import datetime

events = {}

def add_event(event_id, name, description, rewards, start_date, end_date):
    events[event_id] = {
        'name': name,
        'description': description,
        'rewards': rewards,
        'start_date': start_date,
        'end_date': end_date
    }

def remove_event(event_id):
    if event_id in events:
        del events[event_id]

def get_active_events():
    now = datetime.datetime.now()
    active_events = {eid: event for eid, event in events.items() if event['start_date'] <= now <= event['end_date']}
    return active_events

events = {}

def add_event(event_id, name, description, characters, rewards):
    events[event_id] = {
        'name': name,
        'description': description,
        'characters': characters,
        'rewards': rewards,
        'active': False
    }

def start_event(event_id):
    if event_id in events:
        events[event_id]['active'] = True

def end_event(event_id):
    if event_id in events:
        events[event_id]['active'] = False

def get_active_events():
    return {eid: evt for eid, evt in events.items() if evt['active']}
