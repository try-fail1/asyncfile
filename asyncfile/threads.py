import threading
from collections import deque

class TRunner(threading.Thread):
    que = deque(maxlen=20)
    lq = deque(maxlen=2)
    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.loop = None
    def run(self) -> None:
        while self.loop is None:
            try:
                self.loop = self.lq.pop()
            except IndexError:
                continue
        while self.loop is not None:
            try:
                popped = self.que.pop()
            except IndexError:
                continue
            fut, func, args, kwargs = popped
            try:
                self.loop.call_soon_threadsafe(fut.set_result, func(*args, **kwargs))
            except Exception as e:
                self.loop.call_soon_threadsafe(fut.set_exception, e)

async def threadwork(*args, **kwargs):
    func = kwargs.pop('func')
    loop = kwargs.pop('loop')
    fut = loop.create_future()
    TRunner.que.append((fut, func, args, kwargs))
    return await fut

TRunner().start()
