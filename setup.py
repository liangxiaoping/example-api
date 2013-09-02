#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#

from setuptools import find_packages, setup
__version__="0.1.0"
from os import path

with open('tools/pip-requires', 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

setup(
    name='example-api',
    version=__version__,
    description='example-api',
    author='example-api Team',
    author_email='example-api@example.com',
    url='http://example-api.com',
    packages=find_packages(exclude=['tests', 'benchmarks']),
    install_requires=requires,
    zip_safe=False,
    long_description=open(
        path.join(
            path.dirname(__file__),
            'README'
        )
    ).read(),
    test_suite='nose.collector',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
        "Topic :: Software Development :: System :: Python Systems",
        "Intended Audience :: Developers",
        "Development Status :: 1 - Beta",
    ],

    scripts=[
        'bin/example-api',
        ],

    entry_points={
        'example.api.v1':[
            'messages=example.api.v1.messages:blueprint',
            ],
        'example.storage':[
            'redis=example.storage.impl_redis:RedisStorage',
            ],
        },

)
