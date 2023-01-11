from setuptools import setup, find_packages
from src.realty.version import __version__

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
license_text = (this_directory / "LICENSE").read_text()

setup(
    name='py-realty',
    version=__version__,
    description='Python real estate scraping library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=license_text,
    author='Jakub Polanowski',
    url='https://github.com/JakubPolanowski/PY-Realty',
    python_requires=">=3.10, <4",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "beautifulsoup4>=4.11.1",
        "numpy>=1.24.0",
        "requests>=2.28.1",
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    project_urls={
        # "Documentation": "#TODO",
        "Source": "https://github.com/JakubPolanowski/PY-Realty",
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ],
)
