import re
from distutils.core import setup

__version__ = "0.1a"

setup(
    name = "Typecast",
    version = __version__,
    packages = ['typecast', 'typecast.lib'],

    requires = [],
    install_requires = [],

    package_data = {
        '': ['*.md'],
    },

    # metadata for upload to PyPI
    author = "Erez Shinan",
    author_email = "erezshin@gmail.com",
    description = "Cast-Oriented Programming",
    license = "MIT/GPL",
    keywords = "cast typecast",
    url = "https://github.com/erezsh/typecast",   # project home page, if any
    download_url = "https://github.com/erezsh/typecast/tarball/master",
    long_description='''
Typecast is an experimental python library for defining casts (transformations) between different classes.

Casts:
* Defined as Type1 -> Type2
* Are applied to instances (in this example, instances of Type1)
* Connect into cast-chains (shortest path is chosen)
    ''',

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
    ],

)

