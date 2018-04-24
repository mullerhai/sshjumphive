#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='ssh_jump_hive',
    version='0.2.3',
    description=(
        'ssh_jump_hive is a tools could  jump the jump machine  to connect hive get hive data to pandas dataframe'
    ),
    long_description=open('README.rst').read(),
    author='mullerhai',
    author_email='hai710459649@foxmail.com',
    maintainer='muller helen',
    maintainer_email='hai710459649@foxmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/mullerhai/sshjumphive',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'pandas>=0.20.3',
        'PyHive>=0.5.1',
        'paramiko>=2.4.1',
        'selectors>=0.0.14',
        'sasl>=0.2.1',
        'thrift>=0.11.0',
        'thrift-sasl>=0.3.0',
        'hdfs>=2.1.0',
        'sklearn-pandas>=1.6.0',
        'scikit-learn>=0.19.1',

    ],
)
