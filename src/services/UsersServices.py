from src.services.ConnectionDatabase import ConnectionDatabase

DATABASE = 'db_files/PYFY.db'
conn = ''
BASEDEF = 'users'
FORMAT = ConnectionDatabase.formatter

class UsersServices:

    def __init__(self, directory):
        global conn
        if not directory.__contains__(''):
            conn = ConnectionDatabase(directory)
        else:
            conn = ConnectionDatabase(DATABASE)

    @staticmethod
    def checkExist(id):

        if conn.getName(BASEDEF, id).__contains__("[]"):
            return False
        else:
            return True

    @staticmethod
    def getStep(id):
        return FORMAT(conn.getStep(BASEDEF, id))

    @staticmethod
    def getName(id):
        return FORMAT(conn.getName(BASEDEF, id))

    @staticmethod
    def getQuestions(id):
        return FORMAT(conn.getQuestions(BASEDEF, id))



