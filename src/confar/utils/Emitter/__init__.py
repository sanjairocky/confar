from datetime import datetime


class Event:
    def __init__(self, event, data):
        self.event = event
        self.timestamp = datetime.now()
        self.data = data


class EventEmitter:
    def __init__(self):
        self.listeners = {}

    def on(self, event, callback):
        if event in self.listeners:
            self.listeners[event].append(callback)
        else:
            self.listeners[event] = [callback]
        return self

    def emit(self, event, data):
        event_data = Event(event=event, data=data)
        if event in self.listeners:
            for listener in self.listeners[event]:
                listener(event_data)
        if "*" in self.listeners:
            for listener in self.listeners["*"]:
                listener(event_data)
        return self

    def off(self, event, callback):
        if event in self.listeners and callback in self.listeners[event]:
            self.listeners[event].remove(callback)
        return self

    def off_any(self, event):
        if event in self.listeners:
            del self.listeners[event]
        return self

    def on_any(self, callback):
        self.on("*", callback)


# # Example usage
# def on_event_fired(event, data):
#     print(f"Event '{event}' fired with data: {data}")

# emitter = EventEmitter()

# emitter.on("custom_event", on_event_fired)
# emitter.on_any(on_event_fired)

# emitter.emit("custom_event", "Some data")
# emitter.emit("another_event", "Other data")
