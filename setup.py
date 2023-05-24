import re

from setuptools import setup

# inspired by https://github.com/Rapptz/discord.py/blob/master/setup.py

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('tipme/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

# readme = ''
# with open('README.md') as f:
#     readme = f.read()

packages = [
    'tipme',
]

setup(
    name='tipme',
    author='STACiA',
    url='https://github.com/staciax/tipme',
    project_urls={
        'Issue tracker': 'https://github.com/staciax/tipme/issues',
    },
    version=version,
    packages=packages,
    license='MIT',
    description='A Unofficial python wrapper for TipMe API',
    # long_description=readme,
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8.0',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
