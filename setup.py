from setuptools import setup

setup(
    name='tin',
    version='0.0.1',
    py_modules=['tin'],
    install_requires=['Click', 'requests', 'py'],
    entry_points='''
        [console_scripts]
        tin=tin:cli
    '''
)
