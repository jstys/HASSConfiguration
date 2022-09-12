from util import logger

callbacks = {}

def dispatch(event):
    event_name = event.__class__.__name__
    for tup in callbacks.get(event_name, []):
        callback = tup[0]
        event_filter = tup[1]
        if not event_filter or event_filter(event):
            callback(event)

def register_callback(callback, event_name, event_filter=None):
    global callbacks
    
    if event_name not in callbacks:
        callbacks[event_name] = []
        
    callbacks[event_name].append((callback, event_filter))
    logger.debug("Registered callback for {}".format(event_name))
    
def clear_callbacks():
    global callbacks
    
    callbacks.clear()