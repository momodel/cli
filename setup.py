from setuptools import setup, find_packages

setup(
    name ='mo',
    version = '0.1.0',
    packages =find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'requests-toolbelt'
    ],
    entry_points='''
        [console_scripts]
        mo=mopackage.scripts.cli:start
    '''
)