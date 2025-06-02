from setuptools import setup, find_packages

setup(
    name='PyDLLManager',
    version='1.2.0',
    author='AtomixCore',
    author_email='atomixcore@proton.me',
    description='A library for effortlessly loading DLL files in Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AtomixCore/PyDLLManager',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
