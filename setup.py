from setuptools import setup, find_packages

setup(
    name='expense-tracker',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'expense-tracker=src.__main__:main',
        ],
    },
)
