from setuptools import setup, find_packages
from os import path

DIR = path.dirname(path.abspath(__file__))
INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

setup(
    name='freestyle_utils',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
,
    description="Freestyle toolbox",
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=INSTALL_PACKAGES,
    version='0.0.2',
    url='https://github.com/chibinjiang/freestyle_utils',
    author='zhibin.jiang',
    author_email='jiangzhibin2014.xujie@gmail.com',
    keywords=['utils', 'freestyle'],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-sugar'
    ],
    package_data={
        # include json and pkl files
        '': ['*.json', 'models/*.pkl', 'models/*.json'],
    },
    include_package_data=True,
    python_requires='>=3'
)

