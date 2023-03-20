from setuptools import setup

setup(
    name='DaLaS',
    version='0.1.1',
    packages=['dalas', 'dalas.models'],
    url='https://github.com/TheRealMizAL/DaLaS',
    license='GNU GPL v3.0',
    author='kov20',
    author_email='amizurenko2002@gmail.com',
    description='Fully customizable asynchronous Donation Alerts API',
    install_requires=[
        'pydantic>=1.9.1',
        'loguru>=0.6.0',
        'PyYAML>=6.0',
        'websockets>=10.3',
        'aiohttp>=3.8.1'
    ]
)
