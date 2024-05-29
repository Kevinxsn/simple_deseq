import os
from setuptools import setup, find_packages

# version-keeping code based on pybedtools
curdir = os.path.abspath(os.path.dirname(__file__))
MAJ = 1
MIN = 0
REV = 0
VERSION = '%d.%d.%d' % (MAJ, MIN, REV)
with open(os.path.join(curdir, 'simple_deseq/version.py'), 'w') as fout:
        fout.write(
            "\n".join(["",
                       "# THIS FILE IS GENERATED FROM SETUP.PY",
                       "version = '{version}'",
                       "__version__ = version"]).format(version=VERSION)
        )

setup(
    name='simple_deseq',
    version=VERSION,
    description='CSE185 Project', # TODO add longer description
    author='Kevin Xu, Longmei Zhang, Zhirui',
    author_email='loz001@ucsd.edu',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            'simple_deseq=simple_deseq.cli:main'
        ],
    },
)
