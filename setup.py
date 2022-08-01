import setuptools
import pathlib
import re

def get_version():
    p = pathlib.Path('asyncfile/__init__.py')
    with p.open(mode='r', encoding='utf8', errors='replace') as f:
        version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
        return version

def get_readme():
    p = pathlib.Path('README.rst')
    with p.open(mode='r', encoding='utf8', errors='replace') as f:
        readme = f.read()
    return readme

setuptools.setup(
    name='asyncfile',
    version=get_version(),
    description='An asynchronous file handling module.',
    packages=['asyncfile'],
    url='https://github.com/try-fail1/asyncfile',
    long_description=get_readme(),
    long_description_content_type='text/x-rst',
    author='Ryan',
    license='MIT',
    include_package_data=True,
    python_requires='>=3.6.0',
    keywords=['python', 'asyncio', 'fileio'],
    classifiers=[
        'Framework :: AsyncIO',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Utilities'
    ]
)
