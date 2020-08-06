from asyncio import AbstractEventLoop
from typing import (
    Optional, Iterable,
    AsyncIterator, Callable
)
from collections.abc import Coroutine
from functools import wraps

from .threads import threadwork

Loop = Optional[AbstractEventLoop]

def add_async_methods(names: Iterable):
    def the_class(cls):
        for i in names:
            setattr(cls, i, set_async(i))
        return cls
    return the_class

def add_properties(names: Iterable):
    def classy(cls):
        for i in names:
            setattr(cls, i, set_property(i))
        return cls
    return classy

def set_async(method_name: str) -> Callable:
    async def inner(self, *args, **kwargs):
        method_impl = getattr(self._hidden, method_name)
        return await threadwork(*args, func=method_impl, loop=self._loop, **kwargs)
    return inner

def set_property(property_value: str) -> property:
    
    def getit(self):
        return getattr(self._hidden, property_value)
    
    def setit(self, value):
        setattr(self._hidden, property_value, value)
    
    def delit(self, value):
        delattr(self._hidden, property_value, value)
    
    return property(getit, setit, delit)

class AsyncMixin:
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        f = await self.readline()
        if not f:
            raise StopAsyncIteration
        return f
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *exc) -> None:
        await self.close()

class AwaitedForYou(Coroutine):
    
    __slots__ = ('coro', 'ret')
    
    def __init__(self, coro):
        self.coro = coro
        self.ret = None
    
    def send(self, val):
        return self.coro.send(val)
    
    def throw(self, typ, val=None, tb=None):
        return super().throw(typ, val, tb)
    
    def close(self) -> None:
        return self.coro.close()
    
    def __await__(self):
        return self.coro.__await__()
    
    async def __aenter__(self):
        self.ret = await self.coro
        return self.ret
    
    async def __aexit__(self, *exc) -> None:
        await self.ret.close()
        self.ret = None
    
    def __aiter__(self) -> AsyncIterator:
        async def asyncgen():
            f = await self.coro
            async for i in f:
                yield i
        return asyncgen()
    
    # Ultimately, implementing `__anext__`
    # Is not reasonably acheivable here

def make_async(func):
    @wraps(func)
    def different(*args, **kwargs):
        return AwaitedForYou(func(*args, **kwargs))
    return different