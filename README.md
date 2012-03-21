GSkel
===============================================================================
gskel is a cli project skeleton tool designed for commandline buffs and people
who generally despise using a single IDE application solution for software
development.

More info
------------------------------------------------------------------------------
GSkel offers one of the most prominent basic features of any IDE: templates, or
project skeletons. The main idea behind it is to have a commandline application
that can generate a new project in whatever language without creating a huge
mess of unnecessary files.

Dependencies
------------------------------------------------------------------------------
GSkel dependencies:

- Python (Developed and tested on python 2.6.5)
- lxml - libxml python library
- PyYAML - YAML library for python
- argparse - command line parsing library for python

Quick Install Guide
==============================================================================
Instructions on how to set up certain dependencies may differ depending on the
platform:

OS X
------------------------------------------------------------------------------
Grab `libxml2` and `PyYAML` you will need them, along with the python bindings.
The recommended way to do this is using `pip`.

    STATIC_DEPS=true sudo pip install lxml
    sudo pip install pyyaml

Then grab the code from git:

    git clone git://github.com/hk0i/gskel.git

The recommended install method (for the time being) is to symlink the `gskel`
script in a local `bin` directory in your path:

    cd gskel
    ln -s gskel ~/bin/.

Assuming `~/bin` is in your path you should now be able to run gskel on the
command line:

    $ gskel
    usage: gskel [-h] [--version] [-v] [-l] [-p PROJECT_NAME] [-o OUTPATH]
             lang directive [params [params ...]]
    gskel: error: too few arguments