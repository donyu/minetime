## Minetime - PLT Project Spring '13 ##

Minetime, a language for creating structures in Minecraft.
---------------------------------------------------------
Environment Set Up Instructions

We will be working with python for this assignment so make sure you have pip and easy_install already on your computer.

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

Tools
-----
* http://www.dabeaz.com/ply/

Please look inside lex_yacc folder for examples of ply programs to base off of.

Members
-------
* Project Manager:            Mirza
* Language and Tools Guru:    Tanay
* System Architect:           Don
* System Integrator:          Patrice
* Tester/Validator:           Stephen
