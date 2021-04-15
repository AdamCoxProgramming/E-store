from Interface.CustomerInterface import startProgram
from Datastore.CreateTables import dropAllTables,createTables

def resetData():
    dropAllTables()
    createTables()

#resetData()

startProgram(False)