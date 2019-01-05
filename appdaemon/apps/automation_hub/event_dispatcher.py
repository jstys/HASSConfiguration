import logger

callbacks = {}

def dispatch(event):
    event_name = event.__class__.__name__
    logger.info("Dispatching {} callbacks for {}".format(event_name, len(callbacks.get(event_name, []))))
    for callback in callbacks.get(event_name, []):
        callback(event)

def register_callback(callback, event_name):
    global callbacks
    
    if event_name not in callbacks:
        callbacks[event_name] = []
        
    callbacks[event_name].append(callback)
    logger.info("Registered callback for {}".format(event_name))
    
def clear_callbacks():
    global callbacks
    
    callbacks.clear()