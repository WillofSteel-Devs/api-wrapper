from setuptools import setup
import re

VERSION = "0.2"

requirements = [
    "aiohttp>=3.7.4,<4"
]

extras_require = {
    'docs': [
        'sphinx==4.4.0',
        'sphinxcontrib_trio==1.1.2',
        # TODO: bump these when migrating to a newer Sphinx version
        'sphinxcontrib-websupport==1.2.4',
        'sphinxcontrib-applehelp==1.0.4',
        'sphinxcontrib-devhelp==1.0.2',
        'sphinxcontrib-htmlhelp==2.0.1',
        'sphinxcontrib-jsmath==1.0.1',
        'sphinxcontrib-qthelp==1.0.3',
        'sphinxcontrib-serializinghtml==1.1.5',
        'typing-extensions>=4.3,<5',
        'sphinx-inline-tabs==2023.4.21',
    ],
}

packages = [
    'willofsteel',
    'willofsteel.types'
]

readme = ''
with open('README.rst') as f:
    readme = f.read()

setup(
    name='willofsteel',
    author='ItsNeil',
    url='https://wrapper.willofsteel.me',
    version=VERSION,
    packages=packages,
    license='MIT',
    description='A Python wrapper for the Discord API',
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires='>=3.8.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)