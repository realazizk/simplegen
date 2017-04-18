#   Simplegen is a simple program to generate static sites
#   Copyright (C) 2016  Mohamed Aziz Knani


from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session='hey')
reqs = [str(ir.req) for ir in install_reqs]


setup(
    name='simplegen',
    version='1.0.1',
    install_requires=reqs,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    url='https://github.com/mohamed-aziz/simplegen',
    license='GPLV3',
    author='Mohamed Aziz Knani',
    author_email='medazizknani@gmail.com',
    description='Simple site generator.',
    packages=['simplegen'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'makesite=simplegen.cli:makesite',
            'initsite=simplegen.cli:initsite'
        ]
    },
    package_date={
        '': ['requirements.txt', 'readme.md', 'requirements_dev.txt']
    },

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='static website generator simple markdown',

)
