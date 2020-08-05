import doctest
import tempfile
import unittest
import asyncfile
import asyncio

unit = doctest.DocTestSuite(module=asyncfile,
    globs={'random_file': tempfile.mkstemp()[0]})