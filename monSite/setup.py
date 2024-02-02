from setuptools import setup

setup(
    name="monSite",
    version="0.0.1",
    description="Mon site",
    author="Charles",
    author_email="pi.dubs@sfr.fr",
    packages=["monSite"],  # would be the same as name
    install_requires=[
        "flask",
    ],  # external packages acting as dependencies
)