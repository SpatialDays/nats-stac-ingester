from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='stac_ingester',
    packages=['stac_ingester'],
    python_requires='>=3.8, <4',
    install_requires=required
)