#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'london',
    version = '0.0.1',
    description = 'London Mobile Guide',
    author = 'James Arthur',
    author_email = 'username: thruflo, domain: gmail.com',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ],
    license = 'http://unlicense.org/UNLICENSE',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe = False,
    install_requires=[
        'weblayer',
        'PasteScript',
        'WSGIUtils',
        'SQLAlchemy==0.6.7',
        'pyyaml',
        'setuptools-git==0.3.4'
    ],
    entry_points = {
        'setuptools.file_finders': [
            'foo = setuptools_git:gitlsfiles'
        ],
        'paste.app_factory': [
            'main=london.app:factory'
        ]
    }
)
