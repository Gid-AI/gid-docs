from setuptools import setup, find_packages

setup(
    name='gid8_trainer',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'torch==2.3',
        'transformers',
        'google-cloud-storage'
    ]
)