import sys
import pytest
import os

"""
test basic functioning of the program
"""


@pytest.fixture(scope='session')
def make_config(tmpdir_factory):
    # reusing function cause decorators syntax sugar lol :)
    def initsite(funfun, input_dir, output_dir):
        with open(funfun, 'w') as myfile:
            myfile.writelines(
                ['CONTENT_DIR=\'%s\'\n' % input_dir,
                 'OUTPUT_DIR=\'%s\'\n' % output_dir,
                 'THEME_DIR=\'%s\'\n' % os.path.join(os.getcwd(), 'example_theme')
                ]
            )

    dire = tmpdir_factory.mktemp("somedirectory")
    funfun = str(dire.join('sconfig.py'))
    initsite(
        funfun,
        'test_input',
        'test_output'
    )

    # register testing directory path
    sys.path.append(
        str(dire)
    )
    import sconfig
    return funfun, sconfig


def test_init_site(make_config):
    a, b = make_config
    assert b.CONTENT_DIR == 'test_input'
    assert b.OUTPUT_DIR == 'test_output'


def test_make_site(make_config):
    a, b = make_config

    def makesite():
        from simplegen.simplegen import make
        make()

    makesite()
