# djangoAPI/setup.py
from setuptools import setup, find_packages

setup(
    name='django-my-djangoapi',
    version='0.1.0',
    description='The entire djangoAPI project as a reusable app.',
    author='Dhara Savani',
    author_email='dsm952004@gmail.com',
    include_package_data=True,
    packages=find_packages(), # This will find all packages within djangoAPI
    install_requires=[
        'django>=3.0,<5.0',
        'djangorestframework>=3.0,<4.0',
    ],
)