from setuptools import setup, find_packages

setup(
    name='plexec',
    version='1.0.0',
    description='Module to execute commands on multiple hosts',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/plexec',  # Replace with your actual URL
    packages=find_packages(),
    install_requires=[
        'parallel-ssh',
    ],
    entry_points={
        'console_scripts': [
            'plexec=plexec:main',  # Assuming your main function is in plexec.py
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)