asyncfile
===========

A simple and up-to-date module that enables compatibility with asyncio and fileIO operations in Python.

Purpose
--------

Operating on files in Python is a synchronous activity. When normally operating on file this does not
cause any problems. However, when files are tampered with in code that also runs the asyncio event
loop, this can cause the `asyncio <https://docs.python.org/3/library/asyncio.html>`_ `event loop <https://docs.python.org/3/library/asyncio-eventloop.html>`_ to block. This negatively effects the program's performance
and should therefore be avoided. The ``asyncfile`` module avoids this problem by running the file operations in a separate
thread so that the event loop is not as harshly affected.

Features
----------

* *async* and *await* syntax is used
* There is almost complete coverage of the `io <https://docs.python.org/3/library/io.html#module-io>`_ module's classes
* The syntax and utility is similar to the built-in Python `open <https://docs.python.org/3/library/functions.html#open>`_ function and the built-in `io <https://docs.python.org/3/library/io.html#module-io>`_ module
* Lightweight in speed and memory

Installation
-----------------

Installing ``asyncfile`` should be done through `PIP <https://pypi.org/project/pip/>`_:

.. code:: sh

    pip install asyncfile


Open Examples
--------------

If you were to have regular, blocking code, you can easily transition it to ``asyncfile``

**Blocking:**

.. code:: py

    with open('fake_file', 'r') as f:
        print(f.read())

**Non-Blocking:**

.. code:: py

    import asyncfile
    import asyncio

    custom_loop = asyncio.get_event_loop() # You can pass in your own loop

    async def open_file():
        async with asyncfile.open('fake_file', 'r', loop=custom_loop) as f:
            print(await f.read())
    
    custom_loop.run_until_complete(open_file())

These both produce the same results, but one is better suited for asyncio-based code.

IO Examples
--------------

**Blocking:**

.. code:: py
    
    import io

    wrap = io.FileIO('fake_file.txt', 'wb')

    buff = io.BufferedReader(wrap)
    buff.write(b'Random bytes')
    print(buff.fileno())
    print(buff.raw)
    print(buff.readable())
    buff.close()

**Non-Blocking:**

.. code:: py

    import asyncfile
    import asyncio

    async def no_block(file_path):
        wrap = asyncfile.AsyncFileIO(file_path, 'rb')
        buff = asyncfile.AsyncBufferedReader(wrap)
        await buff.read(-1)
        print(await buff.fileno())
        print(buff.raw)
        print(await buff.readable())
        await buff.close()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(no_block('fake_file.txt'))

**Blocking:**

.. code:: py

    import io

    for i in io.FileIO('fake_file.txt'):
        print(i)

**Non-Blocking:**

.. code:: py

    import asyncfile
    import asyncio

    async def async_iteration():
        async for i in asyncfile.AsyncFileIO('fake_file.txt'):
            print(i)
        

