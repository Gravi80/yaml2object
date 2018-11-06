#!/usr/bin/env python

from os import path

from setuptools import setup, find_packages
from setuptools.command.install import install as _install


def read_file(filename):
    with open(path.join(path.dirname(__file__), filename)) as file:
        return file.read()


class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()


if __name__ == '__main__':
    setup(
        name='yaml2object',
        version='1.0.5',
        description='A simple solution that allows dot notation for YAML file.',
        long_description=f"""{read_file('README.md')}""",
        long_description_content_type="text/markdown",
        author='Ravi Sharma',
        author_email='ravi.sharma.cs11@gmail.com',
        license='Apache2',
        url='https://github.com/imravishar/yaml2object',
        keywords=['YAML', 'pyyaml', 'Python YAML', 'python yaml'],
        packages=find_packages(exclude=['tests']),
        classifiers=[
            'Environment :: Console',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Operating System :: OS Independent',
            'License :: OSI Approved :: Apache Software License',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        install_requires=['pyyaml'],
        zip_safe=True,
        cmdclass={'install': install},
    )
