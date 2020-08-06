import asyncio
import io
from os import PathLike
from collections import UserList
from typing import (Optional, Union, Any, Callable, IO, BinaryIO)

from .usefuls import add_async_methods, add_properties, AsyncMixin, Loop
from.threads import TRunner

class ReturnExtended(UserList):
    def extend(self, iterable) -> list:
        self.data.extend(iterable)
        return self.data

_base_meths = ReturnExtended([
    'close', 'fileno', 'flush',
    'isatty','readable', 'seekable',
    'writable', 'tell', 'truncate',
    'readline', 'readlines', 'seek',
    'writelines', 'read', 'write'
])


@add_async_methods(
    _base_meths.extend(['reconfigure', 'detach'])
)
@add_properties(
    ['closed', 'buffer', 'mode',
    'name', 'line_buffering', 'write_through',
    'newlines', 'errors', 'encoding'])
class AsyncTextIOWrapper(AsyncMixin):
    """An asynchronous version of :class:`io.TextIOWrapper`"""
    def __init__(
            self,
            buffer: BinaryIO,
            encoding: Optional[str] = None,
            errors: Optional[str ] = None,
            newline: Optional[str] = None,
            line_buffering: Optional[bool] = False,
            write_through: Optional[bool] = False,
            *,
            loop: Loop = asyncio.get_event_loop()
            ) -> None:
        self._loop = loop
        if isinstance(buffer,
                (AsyncBufferedRandom,
                AsyncBufferedReader,
                AsyncBufferedWriter)):
            buffer = buffer._hidden
        self._hidden = io.TextIOWrapper(
            buffer, encoding, errors, newline,
            line_buffering, write_through)
        TRunner.lq.append(loop)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop
    


@add_async_methods(
    _base_meths.extend(
    ['peek', 'read1', 'readinto1', 'readinto', 'detach']))
@add_properties(['closed', 'raw', 'name', 'mode'])
class AsyncBufferedReader(AsyncMixin):
    
    """An asynchronous version of :class:`io.BufferedReader`"""
    def __init__(
            self, raw: IO,
            buffer_size: Optional[int] = io.DEFAULT_BUFFER_SIZE,
            *, loop: Loop = asyncio.get_event_loop()) -> None:
        self._loop = loop
        if isinstance(raw, AsyncFileIO):
            raw = raw._hidden
        self._hidden = io.BufferedReader(raw, buffer_size)
        TRunner.lq.append(loop)
    
    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop


@add_async_methods(
    _base_meths.extend(['detach', 'read1', 'readinto1', 'readinto']))
@add_properties(['closed', 'raw', 'name', 'mode'])
class AsyncBufferedWriter(AsyncMixin):
    """An asynchronous version of :class:`io.BufferedWriter`"""

    def __init__(
            self, raw: IO, 
            buffer_size: Optional[int] = io.DEFAULT_BUFFER_SIZE,
            *, loop: Loop = asyncio.get_event_loop()) -> None:
        self._loop = loop
        if isinstance(raw, AsyncFileIO):
            raw = raw._hidden
        self._hidden = io.BufferedWriter(raw, buffer_size)
        TRunner.lq.append(loop)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop


@add_async_methods(
    _base_meths.extend(
    ['detach', 'read1', 'readinto1', 'readinto', 'peek']))
@add_properties(['raw', 'closed', 'name', 'mode'])
class AsyncBufferedRandom(AsyncMixin):
    def __init__(
            self, raw: IO,
            buffer_size: Optional[int] = io.DEFAULT_BUFFER_SIZE,
            *, loop: Loop = asyncio.get_event_loop()) -> None:
        self._loop = loop
        if isinstance(raw, AsyncFileIO):
            raw = raw._hidden
        self._hidden = io.BufferedRandom(raw, buffer_size)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop


@add_async_methods(['readall', 'readinto'])
@add_properties(['name', 'mode', 'closefd', 'closed'])
class AsyncFileIO(AsyncMixin):
    
    def __init__(
            self, name: Union[str, bytes, PathLike], mode: str,
            closefd: Optional[bool] = True, opener: Callable[[Any, Any], int] = None,
            *, loop: Loop = asyncio.get_event_loop()) -> None:
        self._hidden = io.FileIO(name, mode, closefd, opener)
        self._loop = loop
    
    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop