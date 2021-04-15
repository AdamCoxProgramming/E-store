from Test.TestCase import runBusinessLayerTests
import Test.InterfaceTest as InterfaceTest
from Datastore.Connection import Connection
import unittest

def runBusinessTests():
    print("--Business Layer Tests--")
    Connection().useTestDatabase()
    runBusinessLayerTests()

def runInterfaceTests():
    print("--Interface Tests--")
    Connection().useTestDatabase()
    suite = unittest.TestLoader().loadTestsFromModule(InterfaceTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

runBusinessTests()
runInterfaceTests()