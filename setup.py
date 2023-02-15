import io
from pathlib import Path
from setuptools import setup, find_packages


requirements = Path("requirements.txt").read_text().splitlines()

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

pkg = "lolexport"
setup(
    name=pkg,
    version="0.1.3",
    url="https://github.com/seanbreckenridge/lolexport",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=(
        """Exports League of Legends Match History data using the RiotGames API"""
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(include=[pkg]),
    package_data={pkg: ["py.typed"]},
    install_requires=requirements,
    extras_require={
        "testing": [
            "mypy",
            "flake8",
        ]
    },
    keywords="api",
    entry_points={"console_scripts": ["lolexport = lolexport.cli:main"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
