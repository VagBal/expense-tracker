from setuptools import setup, find_packages

setup(
    name='expense-tracker',
    version='0.1.0',
    author='Balazs Vagvolgyi',
    author_email='vagvolgyibalazsrobert@gmail.com',
    description='A command line expense tracker app',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'prettytable',  # Add other dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            'expense-tracker=src.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
