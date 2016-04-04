from setuptools import setup
from setuptools.command.test import test as TestCommand


setup(
    name='harlequin',
    version='0.1.0',
    description='Sane MIME library',
    long_description=open('README.rst', 'rb').read().decode('utf8'),
    author='Eeo Jun',
    author_email='packwolf58@gmail.com',
    url='https://github.com/eugene-eeo/harlequin/',
    include_package_data=True,
    package_data={'harlequin': ['LICENSE', 'README.rst']},
    packages=['harlequin'],
    tests_require=[
        'pytest',
        'pytest-localserver',
        'pytest-cov',
    ],
    platforms='any',
    license='MIT',
    zip_safe=False,
)
