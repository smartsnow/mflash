# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path, system
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open
import subprocess
import sys
import webbrowser
import shutil
from mflash import version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install sampleproject
    #
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    name='mflash',  # Required

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version.version,  # Required

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description='MXCHIP Flash Tool',  # Optional

    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,  # Optional

    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type='text/markdown',  # Optional (see note above)

    # This should be a valid link to your project's main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url='https://github.com/smartsnow/mflash',  # Optional

    # This should be your name or the name of the organization which owns the
    # project.
    author='Snow Yang',  # Optional

    # This should be a valid email address corresponding to the author listed
    # above.
    author_email='yangsw@mxchip.com',  # Optional

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='MXCHIP Flash Tool',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(),  # Required

    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. If you
    # do not support Python 2, you can simplify this to '>=3.5' or similar, see
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.5',

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    
    install_requires=['qdarkstyle', 'pyqt5'],  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={  # Optional
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    package_data={  # Optional
        'mflash': ['interface/swj-dp.tcl',
            'interface/stlink-v2.cfg',
            'interface/stlink-v2-1.cfg',
            'interface/jlink_swd.cfg',
            'interface/mxlink.cfg',
            'openocd/osx/libusb-0.1.4.dylib',
            'openocd/osx/openocd_mxos_run',
            'openocd/osx/openocd_mxos_dirname',
            'openocd/osx/openocd_mxos',
            'openocd/osx/libusb-1.0.0.dylib',
            'openocd/osx/libftdi1.2.dylib',
            'openocd/osx/libhidapi.0.dylib',
            'openocd/win/libusb-0-1-4.dll',
            'openocd/win/libusb-1.0.dll',
            'openocd/win/libhidapi-0.dll',
            'openocd/win/openocd_mxos.exe',
            'openocd/win/libftdi1.dll',
            'targets/mx1270.cfg',
            'targets/mx1290.cfg',
            'targets/mx1300.cfg',
            'targets/mx1310.cfg',
            'targets/mx1350.cfg',
            'targets/rtl8762c.cfg',
            'flashloader/ramcode/mx1270.elf',
            'flashloader/ramcode/mx1290.elf',
            'flashloader/ramcode/mx1300.elf',
            'flashloader/ramcode/mx1310.elf',
            'flashloader/ramcode/mx1350.elf',
            'flashloader/ramcode/rtl8762c.elf',
            'flashloader/scripts/cmd.tcl',
            'flashloader/scripts/flash.tcl',
            'resources/flash.png',
            'resources/download.png',
            'resources/log.png',
            'resources/help.png',
            'resources/connection.png',
            'resources/jlink_swd.png',
            'resources/stlink-v2-1.png',
            'resources/stlink-v2.png',
            'resources/mxlink.png',
            'resources/open.png',
        ]
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[
    ],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'mflash=mflash.main:main',
            'mflashi=mflash.ui:main',
        ],
    },

    scripts = ['start.vbs']
)

curdir = path.join(sys.prefix, 'Scripts')
if sys.platform == 'win32':
    # if not register
    exefile = path.join(curdir, 'start.vbs')
    regfile = path.join(curdir, 'rightclick.reg')
    regdata = 'Windows Registry Editor Version 5.00\r\n' + \
        '[HKEY_CLASSES_ROOT\*\shell\mflash]\r\n' + \
        '@="mflash - Download"\r\n' + \
        '[HKEY_CLASSES_ROOT\*\shell\mflash\command]\r\n' + \
        '@=hex(2):' + ',00,'.join([i.to_bytes(1, 'big').hex() for i in ('Wscript.exe "'+exefile+'"' + ' "%1"').encode()]) + ',00'
    open(regfile, 'w').write(regdata)
    system(regfile)

webbrowser.open('https://www.mxchip.com')
