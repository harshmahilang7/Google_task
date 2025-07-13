from setuptools import setup, find_packages

setup(
    name="google-tasks-app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        'gui_scripts': [
            'google-tasks=src.main:main'
        ]
    },
    package_data={
        '': ['assets/icons/*', 'assets/styles/*']
    }
)