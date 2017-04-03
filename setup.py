import os
import sys
from setuptools import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

required = [
    "delegator.py",
    "click",
]

setup(
    name='dinbrief.py',
    version='0.0.1',
    description='Dinbrief made easy',
    long_description='',
    author='Markus Quade',
    author_email='info@markusqua.de',
    url='https://github.com/ohjeah/dinbrief-boilerplate',
    py_modules=['dinbrief'],
    install_requires=required,
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'dinbrief = dinbrief:cli',
        ]
        }
)
