import os
from distutils.core import setup


def long_description():
    fd_path = os.path.join(os.path.dirname(__file__), 'README.rst')
    if not os.path.isfile(fd_path):
        return ''
    with open(fd_path) as fd:
        return fd.read()

setup(
    name='django-dynamicwidgets',
    version='1.0',
    author='Piotr Husiatyński',
    author_email='phusiatynski@gmail.com',
    url='http://github.com/husio/django-dynamicwidgets/',
    long_description=long_description(),
    packages=['dynamicwidgets'],
    license='MIT',
    install_requires=(
        'django>=1.5',
    ),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    )
)
