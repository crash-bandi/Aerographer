from setuptools import find_packages, setup

setup(
    name='aerographer',
    version='1.2.4',
    python_requires='>=3.10',
    install_requires=['boto3 >=1.21.0'],
    package_data={'aerographer': ['*.json',  '*.pyi', '**/*.pyi']},
    packages=find_packages(exclude=['tests'])
)
