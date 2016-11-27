

## simpleGen

simpleGen *is a simple static website/blog generator* I work on, on sundays.

### Installing simplegen.

You can install simpleGen from the Python package index using pip (I maintain this package).
	
	$ pip install simplegen

and then you want to initialize a site, so use:

	$ initsite input_dir output_dir
	
a config file with name sconfig.py will be generated, edit that with what suits you and your theme
you are using.

then you can write you content in markdown in the input_dir, then run:

	$ makesite
	
to actually generate your content.

deploying your website is up to you, I myself use git submodules and github pages.


### Todo

- [ ] Write tests.
- [X] Make a paging system.
- [X] Transform it into a package.
  - [X] Upload it to pypi.
  - [X] Use armin's click.
- [ ] Support Python3.
