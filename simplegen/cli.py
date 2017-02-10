#   Simplegen is a simple program to generate static sites
#   Copyright (C) 2016  Mohamed Aziz Knani


import click


@click.command()
@click.argument('input_dir', nargs=1)
@click.argument('output_dir', nargs=1)
def initsite(input_dir, output_dir):
    with open('sconfig.py', 'w') as myfile:
        myfile.writelines(
            ['CONTENT_DIR=\'%s\'\n' % input_dir,
             'OUTPUT_DIR=\'%s\'\n' % output_dir]
        )


@click.command()
def makesite():
    from .simplegen import make
    make()
