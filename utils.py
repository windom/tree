import functools


def deferred(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        deferrable = args[0]
        if deferrable.flushing:
            func(*args, **kwargs)
        else:
            deferrable.queue_call(func, args, kwargs)
    return decorated


class Deferrable:
    def __init__(self):
        self.calls = []
        self.flushing = False

    def queue_call(self, func, args, kwargs):
        self.calls.append((func, args, kwargs))

    def flush_calls(self):
        self.flushing = True
        for func, args, kwargs in self.calls:
            func(*args, **kwargs)
        self.flushing = False
