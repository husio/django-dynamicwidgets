from distutils.core import setup


setup(
    name='django-dynamicwidgets',
    version='1.0',
    author='Piotr Husiatyński',
    author_email='phusiatynski@gmail.com',
    url='http://github.com/husio/django-dynamicwidgets/',
    packages=['dynamicwidgets'],
    install_requires=(
        'django>=1.5',
    ),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    )
)
