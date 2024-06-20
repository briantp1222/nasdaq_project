from setuptools import setup, find_packages

setup(
    name='nasdaq_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'sqlalchemy',
        'mysql-connector-python',
        'prefect'
    ],
)
