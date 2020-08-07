import unittest
import unittest.mock as um

import asyncfile

async_open = asyncfile.open # This prevents the builtin open from being used
# When using the patch callable

class OpenUp(unittest.IsolatedAsyncioTestCase):
    async def test_general(self):
        mock_returned = um.MagicMock(spec=asyncfile.AsyncTextIOWrapper)
        mock_opener = um.AsyncMock(return_value=mock_returned)
        filer = await mock_opener('file.txt', 'r', encoding='utf8')
        mock_opener.assert_called_once_with('file.txt', 'r', encoding='utf8')
        filer.name = 'file.txt'
        self.assertEqual(filer.name, 'file.txt')
    
    async def test_ctx_manager(self):
        ctx_open = um.MagicMock()
        async with ctx_open('file.txt', 'rb') as f:
            ctx_open.assert_called_once_with('file.txt', 'rb')
            f.read.return_value = b'binary bytes'
            byt = await f.read()
            self.assertIsInstance(byt, bytes)
            self.assertEqual(byt, b'binary bytes')
        f.closed = True
        self.assertTrue(f.closed)
        if f.closed:
            f.read.side_effect = ValueError
        with self.assertRaises(ValueError):
            await f.read()

    async def test_modes(self):
        with um.patch('__main__.async_open', new_callable=um.AsyncMock, spec=True) as aopen:
            f = await aopen('file.txt', 'r', buffering=0)
            aopen.assert_awaited_once_with('file.txt', 'r', buffering=0)
            f.name = 'file.txt'
            f.mode = 'r'
            bufferread = um.MagicMock(spec=asyncfile.AsyncBufferedReader)
            bufferread.mode = f.mode
            bufferread.name = f.name
            self.assertEqual(f.name, bufferread.name)
            self.assertEqual(f.mode, bufferread.mode)
    
    async def test_aiter(self):
        lines = ["Hi", "Bye", "Left"] # Simulates lines from a file
        async def asyncgen():
            for i in lines:
                yield i
        f = um.MagicMock(return_value=asyncgen())
        empty = []
        async for i in f('file.txt', 'r'):
            empty.append(i)
        self.assertListEqual(lines, empty)

unittest.main()