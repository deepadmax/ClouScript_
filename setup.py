from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='ClouScript',
    url='https://github.com/deepadmax/ClouScript',
    author='Maximillian Strand',
    author_email='maximillian.strand@gmail.com',
    # Needed to actually package something
    packages=['clouscript'],
    # Needed for dependencies
    install_requires=[],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='GPLv3',
    description='A basic and easy-to-use programming language parsing library',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)