#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install as _install


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
        version='1.0.0',
        description='A simple solution that allows dot notation for YAML file.',
        long_description='yaml2object is a simple solution that allows dot notation for YAML file.',
        author='Ravi Sharma',
        author_email='ravi.sharma.cs11@gmail.com',
        license='Apache2',
        url='https://github.com/imravishar/yaml2object',
        keywords=['YAML', 'pyyaml', 'Python YAML', 'python yaml'],
        packages=find_packages(exclude=['tests']),
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python',
            'License :: OSI Approved :: Apache Software License',
        ],
        install_requires=['pyyaml'],
        zip_safe=True,
        cmdclass={'install': install},
    )
