#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='PyFunge',
      version='0.5-rc2',
      description='Functional, compliant and optimizing Funge-98 implementation',
      author='Kang Seonghoon',
      author_email='public+pyfunge@mearie.org',
      url='http://mearie.org/projects/pyfunge/',
      packages=find_packages('.'),
      scripts=['pyfunge'],
      zip_safe=False,
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Other',
          'Topic :: Software Development :: Interpreters',
      ],
)

