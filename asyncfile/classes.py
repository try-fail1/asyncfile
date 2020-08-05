import io
import asyncio
from typing import (Optional, Union, IO, Callable, ByteString, List, Sequence)
from pathlib import Path

from .threads import Inject, put_loop_there

class AsyncFileIO:
    """An asynchronous version of :class:`io.FileIO`

    Parameters
    --------------
    
    name: A valid file path of an open file descriptor
    mode: The mode in which the file is opened
    closefd: If this argument is ``True``,
        the ``fd`` passed to ``name`` will be closed with the
        ``AsyncFileIO`` class
    opener: A custom opener

    Examples
    ----------

    .. code-block:: python3

        >>> import asyncfile
        >>> import asyncio

        >>> loop = asyncio.get_event_loop()
        >>> async def filer():
        ...     file = asyncfile.AsyncFileIO(random_file, closefd=False)
        ...     print(file.name)
        ...     print(await file.seekable())
        ...     print(await file.isatty())
        ...     await file.close()
        ...
        3
        'rb'
        True
        False
            
        >>> async def reader_coro():
        ...     open_file = asyncfile.AsyncFileIO(random_file, mode='r+', closefd=False)
        ...     print(await open_file.write(b'Test!'))
        ...     print(await open_file.read())
        ...
        >>> loop.run_until_complete(reader_coro())
        5
        b'Test!'
        
        # Using the class as an asynchronous context manager
        >>> async def async_ctx():
        ...     async with asyncfile.AsyncFileIO(random_file, closefd=False) as f:
        ...         fd = await f.fileno()
        ...        
        ...     # The file is automatically closed

        
    """


    def __init__(self,
                name: Union[str, bytes, int],
                mode: Optional[str] = 'r',
                closefd: Optional[bool] = True,
                opener: Optional[Callable[[Path, int], IO]] = None,
                loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_event_loop()
                ) -> None:
        put_loop_there(loop)
        self.name = name
        self._loop = loop
        self.__hidden = io.FileIO(name, mode, closefd, opener)
        self._injector = Inject(self.__hidden, loop)
    @property
    def mode(self) -> str:
        """The mode that the file is opened with. Non-writable"""
        return self.__hidden.mode
    
    @property
    def closefd(self) -> bool:
        """A non-writable property that shows the ``closefd`` argument
        passed into the constructor"""
        return self.__hidden.closefd
    
    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Returns the event loop object passed in the constructor. Must be
        set at creation time"""
        return self._loop
    
    @property
    def closed(self) -> bool:
        """Shows whether the file is closed or open"""
        return self.__hidden.closed
    
    def __repr__(self) -> str:
        return f"<AsyncFileIO: name={self.name} mode={self.mode} closefd={self.closefd} loop"
    
    async def read(self, size: Optional[int] = -1) -> bytes:
        """An asynchronous version of :meth:`io.FileIO.read`"""
        return await self._injector.do_thread(size, func='read', result=True)
    
    async def readall(self) -> bytes:
        """An asynchronous version of :meth:`io.FileIO.readall`"""
        return await self._injector.do_thread(func='readall', result=True)

    async def readinto(self, b: ByteString) -> int:
        """An asynchronous version of :meth:`io.FileIO.readinto`"""
        return await self._injector.do_thread(b, func='readinto', result=True)

    async def write(self, b: ByteString) -> int:
        """An asynchronous version of :meth:`io.FileIO.write`"""
        return await self._injector.do_thread(b, func='write', result=True)

    async def close(self) -> None:
        """An asychronous version of :meth:`io.FileIO.close`"""
        await self._injector.do_thread(func='close', result=False)

    async def fileno(self) -> int:
        """An asynchronous version of :meth:`io.FileIO.fileno`"""
        return await self._injector.do_thread(func='fileno', result=True)

    async def flush(self) -> None:
        """An asynchronous version of :meth:`io.FileIO.flush`"""
        await self._injector.do_thread(func='flush', result=False)
    
    async def isatty(self) -> bool:
        """An asynchronous version of :meth:`io.FileIO.isatty`"""
        return await self._injector.do_thread(func='isatty', result=True)
    
    async def readable(self) -> bool:
        """An asynchronous version of :meth:`io.FileIO.readable"""
        return await self._injector.do_thread(func='readdable', result=True)
    
    async def readline(self, hint: Optional[int] = -1):
        """An asynchronous version of :meth:`io.FileIO.readline`"""
        return await self._injector.do_thread(func='readline', result=True)
    
    async def readlines(self, hint: Optional[int] = -1) -> List[Union[str, bytes]]:
        """An asynchronous version of :meth:`io.FileIO.readlines`"""
        return await self._injector.do_thread(hint, func='readlines', result=True)

    async def seek(self, offset: int, whence: Optional[int] = io.SEEK_SET) -> int:
        """An asynchronous version of :meth:`io.FileIO.seek`"""
        return await self._injector.do_thread(offset, whence, func='seek', result=True)
    
    async def seekable(self) -> bool:
        """An asynchronous version of :meth:`io.FileIO.seekable`"""
        return await self._injector.do_thread(func='seek', result=True)
    
    async def tell(self) -> int:
        """An asynchronous version of :meth:`io.FileIO.tell`"""
        return await self._injector.do_thread(func='tell', result=True)

    async def truncate(self, size: Optional[int] = None) -> int:
        """An asynchronous version of :meth:`io.FileIO.truncate`"""
        return await self._injector.do_thread(size, func='truncate', result=True)

    async def writable(self) -> bool:
        """An asynchronous version of :meth:`io.FileIO.writable`"""
        return await self._injector.do_thread(func='writable', result=True)
    
    async def writelines(self, lines: Sequence) -> None:
        """An asynchronous version of:meth:`io.FileIO.writelines`"""
        await self._injector.do_thread(func='writelines', result=False)
    
    def __del__(self):
        del self.__hidden
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *exc):
        await self.close()
    
    def __aiter__(self):
        return self
    
    def __anext__(self):
        f = await self.readline()
        if not f:
            raise StopAsyncIteration
        return f
    

class AsyncBufferedReader:
    """An asynchronous version of :class:`io.BufferedReader`"""
    
    def __init__(self, raw: IO, buffer_size: Optional[int] = io.DEFAULT_BUFFER_SIZE,
                loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_event_loop()):
        self._raw = raw
        self._loop = loop
        self.__hidden = io.BufferedReader(raw, buffer_size)
        self._injector = Inject(self.__hidden, loop)
    
    @property
    def raw(self):
        """Exposes the underlying raw stream"""
        return self._raw
    
    @property
    def loop(self):
        """The running event loop"""
        return self._loop
    
    async def peek(self, size: Optional[int] = None):
        """An asynchronous version of :meth:`io.BufferedReader.peek`"""
        stuff = {'func': 'peek', 'result': True}
        if size is not None:
            stuff['size'] = size
        return await self._injector.do_thread(**stuff)
    
    async def read(self, size: Optional[int] = None):
        """An asynchronous version of :meth:`io.BufferedReader.read`"""
        stuff = {'func': 'read', 'result': True}
        if size is not None:
            stuff['size'] = size
        return await self._injector.do_thread(**stuff)
    
    async def read1(self, size: Optional[int] = None):
        """An asynchronous version of :meth:`io.BufferedReader.read1"""
        stuff = {'func': 'read1', 'result': True}
        if size is not None:
            stuff['size'] = size
        return await self._injector.do_thread(**stuff)
    
            