## Minetime - PLT Project Spring '13 ##

Minetime, a language for creating structures in Minecraft.
---------------------------------------------------------
Environment Set Up Instructions

We will be working with python for this assignment so make sure you have pip and
easy_install already on your computer.

1. Create a virtual environment and pip install all requirements
  * pip install virtualenv
  * virtualenv env
  * source env/bin/activate
  * pip install pyyaml
  * pip install ply
  * pip install numpy

2. Go into env/lib/python2.7/site-packages and git clone pymclevel into there
  * git clone https://github.com/mcedit/pymclevel.git
3. Try out test files within test directory and make sure they work
4. Now go through following steps to install mcedit (to view MineCraft maps)
  * git clone --recursive https://github.com/mcedit/mcedit
  * pip install PyOpenGL
  * pip install pygame

NOTE: The author of the library forgot to comment out print statements in a
recent commit (d02d446). Be sure to comment out lines 803-806 to avoid a ton of
prints each time you import pymclevel

Testing
-------
Testing relies on Python's unittest module.

To run a test from commandline

    python -m unittest discover -s  ./tests -p '<pattern>'

    optional -v verbose flag
    <pattern>: name of test, or *_test.py for all

Or just run the all tests bootstrap
    python runtests.py

Note: You cannot run individual tests files with python because they don't have
the parent directory in the environment variables without discover

Tools
-----
* Lex/Yacc: http://www.dabeaz.com/ply/
* System Integrator (setup.py): http://pythonhosted.org/distribute/setuptools.html
* Tester (unittest): http://docs.python.org/2/library/unittest.html

Please look inside lex_yacc folder for examples of ply programs to base off of.

Members
-------
* Project Manager:            Mirza
* Language and Tools Guru:    Tanay
* System Architect:           Don
* System Integrator:          Patrice
* Tester/Validator:           Stephen
