from setuptools import setup, find_packages
import astroplan
import typeguard
import yaml

setup(
    name="Astro",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Las dependencias se leen desde requirements.txt,
        # así que puedes dejar esto vacío si ya las instalaste.
    ],
)