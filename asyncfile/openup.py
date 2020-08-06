import asyncio
import io
from os import PathLike
from typing import (
    Union,
    Optional,
    Callable,
    Any,
)

from .classes import (
    AsyncFileIO,
    AsyncBufferedRandom,
    AsyncBufferedReader,
    AsyncBufferedWriter,
    AsyncTextIOWrapper
)
from .usefuls import Loop, make_async

@make_async
async def open(
    file: Union[str, bytes, int, PathLike],
    mode: Optional[str] = 'r',
    buffering: Optional[int] = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    closefd: Optional[bool] = True,
    opener: Optional[Callable[[Any, Any], int]] = None,
    *,
    loop: Loop = asyncio.get_event_loop()
    ) -> Union[
        AsyncBufferedRandom, AsyncBufferedReader,
        AsyncBufferedWriter, AsyncFileIO,
        AsyncTextIOWrapper]:
    raw_file = AsyncFileIO(name=file, mode=mode, closefd=closefd, opener=opener, loop=loop)
    if buffering == 0: # Buffering is disabled
        return raw_file
    elif 'r' in mode and '+' not in mode:
        if buffering == -1:
            buf = AsyncBufferedReader(raw=raw_file, buffer_size=io.DEFAULT_BUFFER_SIZE, loop=loop)
        else:
            buf = AsyncBufferedReader(raw=raw_file, buffer_size=buffering, loop=loop)
    elif 'r' not in mode and '+' not in mode:
        if buffering == -1:
            buf = AsyncBufferedWriter(raw=raw_file, buffer_size=io.DEFAULT_BUFFER_SIZE, loop=loop)
        else:
            buf = AsyncBufferedWriter(raw=raw_file, buffer_size=buffering, loop=loop)
    elif '+' in mode:
        if buffering == -1:
            buf = AsyncBufferedRandom(raw=raw_file, buffer_size=io.DEFAULT_BUFFER_SIZE, loop=loop)
        else:
            buf = AsyncBufferedRandom(raw=raw_file, buffer_size=buffering, loop=loop)
    else:
        raise RuntimeError("Invalid mode passed")
    if 'b' in mode:
        return buf
    else:
        if buffering == 1:
            a = True
        else:
            a = False
        return AsyncTextIOWrapper(buffer=buf, encoding=encoding, errors=errors,
                                newline=newline, line_buffering=a,
                                write_through=False, loop=loop)

