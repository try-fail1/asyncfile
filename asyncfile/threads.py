import threading
from collections import deque

class RunThis(threading.Thread):
    looq = deque(maxlen=2)
    futq = deque(maxlen=20)
    event = threading.Event()
    def __init__(self) -> None:
        super().__init__(daemon=True)
    def run(self) -> None:
        while self.looq:
            try:
                loop = self.looq.pop()
            except IndexError:
                continue
        while self.futq and 'loop' in locals():
            try:
                popped = self.futq.pop()
            except IndexError:
                continue
            if len(popped) == 3:
                func, args, kwargs = popped
                # For methods that do not return anything
                # Using a future isn't needed
                func(*args, **kwargs)
                self.event.set()
            else:
                fut, func, args, kwargs = popped
                try:
                    loop.call_soon_threadsafe(fut.set_result, func(*args, **kwargs))
                except Exception as e:
                    loop.call_soon_threadsafe(fut.set_exception, e)

RunThis().start()

def put_loop_there(loop):
    RunThis.looq.append(loop)
class Inject:
    def __init__(self, loop, base):
        self.loop = loop
        self.base = base
    async def do_thread(self, *args, **kwargs):
        func = getattr(self.base, kwargs.pop('func'))
        result = kwargs.pop('result')
        if result is False:
            RunThis.futq.append((func, args, kwargs))
            RunThis.event.clear()
            RunThis.event.wait()
        else:
            fut = self.loop.create_future()
            RunThis.futq.append((fut, func, args, kwargs))
            return await fut