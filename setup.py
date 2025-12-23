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

try:
    import roguehostapd.buildutil.buildcommon as buildcommon
    import roguehostapd.buildutil.buildexception as buildexception
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
except buildexception.SharedLibMissError as exobj:
    print("[" + RED + "!" + WHITE + "] " +
          ("The development package for " + exobj.libname +
           " is missing. Please download it and restart the compilation."
           "If you are on Debian-based system: \'apt-get install{}\'.".format(
               "".join(" " + package for package in exobj.packages))))
finally:
    if os.path.isdir('tmp'):
        shutil.rmtree('tmp')
