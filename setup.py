from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session='hey')
reqs = [str(ir.req) for ir in install_reqs]


setup(
    name='simplegen',
    version='0.0.1',
    install_requires=reqs,
    url='https://github.com/mohamed-aziz/simplegen',
    license='GPLV3',
    author='Mohamed Aziz Knani',
    author_email='medazizknani@gmail.com',
    description='Simple site generator for my site.',
    packages=['simplegen'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'makesite=simplegen.cli:makesite',
            'initsite=simplegen.cli:initsite'
        ]
    },
)
