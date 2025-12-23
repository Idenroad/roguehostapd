"""
Module for setup hostapd shared library
"""

import shutil
import os
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext

# Avoid importing the package at setup time (pip builds in isolated env).
# Define minimal terminal color constants here instead of importing
# `roguehostapd.config.hostapdconfig` which isn't importable during build.
WHITE = "\033[0m"
RED = "\033[31m"

# define project information
NAME = 'roguehostapd'
PACKAGES = [
    'roguehostapd', 
    'examples', 
    'roguehostapd.config', 
    'roguehostapd.buildutil'
]
PACKAGE_DIR = {'roguehostapd': 'roguehostapd'}
PACKAGE_DATA = {'roguehostapd': ['config/hostapd.conf', 'config/config.ini']}
VERSION = '1.2.0'
DESCRIPTION = 'Hostapd wrapper for hostapd - Python 3.13+ modernized by idenroad'
URL = 'https://github.com/idenroad/roguehostapd'
AUTHOR = 'idenroad (fork), Anakin (original)'
PYTHON_REQUIRES = '>=3.8'

# Try to import build helpers; if unavailable, fall back to a pure-Python install
buildcommon = None
buildexception = None
try:
    import roguehostapd.buildutil.buildcommon as buildcommon
    import roguehostapd.buildutil.buildexception as buildexception
except Exception:
    buildcommon = None
    buildexception = None

if buildcommon is not None:
    try:
        EXT_MODULE = buildcommon.get_extension_module()
        setup(
            name=NAME,
            packages=PACKAGES,
            package_dir=PACKAGE_DIR,
            package_data=PACKAGE_DATA,
            version=VERSION,
            description=DESCRIPTION,
            url=URL,
            author=AUTHOR,
            python_requires=PYTHON_REQUIRES,
            install_requires=[],
            zip_safe=False,
            cmdclass={
                'build_ext': build_ext,
                'install': install
            },
            ext_modules=EXT_MODULE,
            classifiers=[
                'Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9',
                'Programming Language :: Python :: 3.10',
                'Programming Language :: Python :: 3.11',
                'Programming Language :: Python :: 3.12',
                'Programming Language :: Python :: 3.13',
                'Operating System :: POSIX :: Linux',
            ],
        )
    except Exception as exc:
        # If the build helpers signalled a missing shared lib, print a readable message
        if buildexception is not None and isinstance(exc, buildexception.SharedLibMissError):
            exobj = exc
            print("[" + RED + "!" + WHITE + "] " +
                  ("The development package for " + exobj.libname +
                   " is missing. Please download it and restart the compilation."
                   "If you are on Debian-based system: \'apt-get install{}\'.".format(
                       "".join(" " + package for package in exobj.packages))))
        else:
            raise
else:
    # No build helpers available; install without compiled extensions
    setup(
        name=NAME,
        packages=PACKAGES,
        package_dir=PACKAGE_DIR,
        package_data=PACKAGE_DATA,
        version=VERSION,
        description=DESCRIPTION,
        url=URL,
        author=AUTHOR,
        python_requires=PYTHON_REQUIRES,
        install_requires=[],
        zip_safe=False,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Programming Language :: Python :: 3.13',
            'Operating System :: POSIX :: Linux',
        ],
    )

# cleanup temporary build directory if present
if os.path.isdir('tmp'):
    shutil.rmtree('tmp')
