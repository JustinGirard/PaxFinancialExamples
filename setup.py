import unittest

test_suite = unittest.defaultTestLoader.discover("./tests",pattern='tests_*.py')
unittest.TextTestRunner(verbosity=2).run(test_suite)
