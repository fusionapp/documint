from setuptools import find_packages, setup



setup(
    name="Documint",
    version="1.0",
    packages=find_packages() + ['twisted.plugins'],
    install_requires=['Twisted', 'lxml'],
    include_package_data=True)
