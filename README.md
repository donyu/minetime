## Minetime - PLT Project Spring '13 ##

Minetime, a language for creating structures in Minecraft.
---------------------------------------------------------

TODO
----

* Make grammar handle statement like if (x>3) or if (x==3)
* Update grammar to allow class methods in if statments
* Traversal for if statments
* Traversal for if else
* Make grammar handle elif

Environment Set Up Instructions
-------------------------------
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

To run a test from commandline, GO INTO test/ (YOU MUST BE IN TEST TO RUN THE 
UNITTESTS---DUE TO RELATIVE FILE PATHS) and run each *_test.py with python.

To run all the tests 

    python runtests.py

NOTE: Imperative that you are in the tests/ directory to run any tests!!

Python also has a CLI method of testing individual classes and methods within
a class following the format

    python -m unittest test_module.TestClass.test_method

    TestClass and test_method being optional

For example, to test the test_0_bug method of TestYaccing in yaccing_test.py,
you would run

    python -m unittest yaccing_test.TestYaccing.test_0_bug

This way, we can save all our test cases as well as keep them modular.

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
