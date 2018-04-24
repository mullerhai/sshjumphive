import codecs
import os

from setuptools import setup, find_packages

# See this web page for explanations:
# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
PACKAGES = ["ssh_jump_hive"]
KEYWORDS = ["hive", "ssh-tunnel", "hfds", "machine learning"]
CLASSIFIERS = [
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Scientific/Engineering",
]
# Project root
ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
    name="ssh_jump_hive",
    description="ssh_jump_hive is a tools could  jump the jump machine  to connect hive get hive data to pandas dataframe",
    license="Apache 2.0",
    url='https://github.com/mullerhai/sshjumphive',
    version="0.2.8",
    author="mullerhai",
    author_email="hai710459649@foxmail.com",
    maintainer="muller helen",
    maintainer_email="hai710459649@foxmail.com",
    long_description=open('README.rst').read(),
    keywords=KEYWORDS,
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    zip_safe=False,
    platforms=["all"],
    include_package_data=True,
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


