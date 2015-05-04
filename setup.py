from setuptools import find_packages, setup



setup(
    name="Documint",
    version="15.5.0",
    url="https://github.com/fusionapp/documint",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Markup :: HTML',
        ],
    packages=find_packages() + ['twisted.plugins'],
    install_requires=['Twisted', 'lxml'],
    include_package_data=True)
