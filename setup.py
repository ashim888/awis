from setuptools import setup, find_packages
# from codecs import open
# from os import path


# here = path.abspath(path.dirname(__file__))
# # Get the long description from the README file
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    # Application name:
    name="myawis",

    # Version number (initial):
    version="0.2.4",

    # Application author details:
    author="Ashim Lamichhane",
    author_email="punchedrock@gmail.com",

    # Packages
    packages=['myawis'],
    # data_files
    data_files=[('awis', ['LICENSE.txt', 'README.rst'])],
    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/ashim888/awis",
    # Keywords
    keywords='python awis api call',
    #
    license='GNU General Public License v3.0',
    description="A simple AWIS python wrapper",
    long_description=open('README.rst').read(),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: Public Domain',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
    ],
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml",
	"xmltodict"
    ],
    entry_points={
        'console_scripts': [
            'myawis=myawis:main',
        ],
    },
)
