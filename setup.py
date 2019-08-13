from setuptools import setup

setup(
    name ='mo',
    version = '0.1.0',
    py_modules=['cli', 'httprequests'],
    install_requires=[
        'Click',
        'requests',
        'requests-toolbelt'
    ],
    entry_points={
        'console_scripts': [
            'mo = cli:start'
        ]
    }
)