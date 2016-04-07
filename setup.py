import versioneer
from setuptools import find_packages, setup



setup(
    name="Documint",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
    install_requires=['Twisted[tls]', 'lxml>=3.6.0'],
    include_package_data=True)
