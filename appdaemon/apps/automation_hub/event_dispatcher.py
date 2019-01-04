callbacks = {}

def dispatch(event):
    event_name = event.__class__.__name__
    for callback in callbacks.get(event_name, []):
        callback(event)

def register_callback(event_name, callback):
    if event_name not in callbacks:
        callbacks[event_name] = []
        
    callbacks[event_name].append(callback)
    
def clear_callbacks():
    callbacks.clear()