import unittest
import sys
import os

# Adds some path to sys environment
# sys.path.insert(0, os.path.abspath('.'))

if __name__ == "__main__":
    # Discovers all tests in ./tests folder
    all_tests = unittest.TestLoader().discover('./tests', pattern="*_test.py")
    unittest.TextTestRunner(verbosity=2).run(all_tests)
