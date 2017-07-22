import MySQLdb

import config
import bot


def execStoreProcedure(procedureName, *args):
    db = MySQLdb.connect(**config.dbConnection)

    cursor = db.cursor()
    cursor.callproc(procedureName, args)
    result = cursor.fetchall()

    cursor.close()
    db.commit()
    db.close()
    return result


def deleteUser(telegramID):
    execStoreProcedure('DELETE_USER', telegramID)


def getListOfUsers():
    return execStoreProcedure('LIST_OF_USERS')


def addUserProblemHistory(telegramID, problemID):
    execStoreProcedure('ADD_USER_PROBLEM_HISTORY', telegramID, problemID)


def getMem():
    return execStoreProcedure('GET_MEM')

def addIssue(telegramID, issue):
    execStoreProcedure('ADD_ISSUE', telegramID, issue)

def addUser(message):
    execStoreProcedure('ADD_NEW_USER', message.chat.id, message.chat.username)


def getRandomEgeNumber():
    return (execStoreProcedure('GET_RANDOM_TASK_NUMBER')[0][0])


def getProblemInfoAndHashtags(problemID):
    return ' '.join("{}".format(i[0]) for i in execStoreProcedure('GET_PROBLEM_INFO_AND_HASHTAGS', [problemID]))


def getEgeProblem(msg, egeNumber=None, problemID=None):
    if egeNumber:
        record = execStoreProcedure('GET_RAND_PROBLEM_BY_EGE_NUMBER', [egeNumber])[0]
    else:
        record = execStoreProcedure('GET_PROBLEM_BY_PROBLEM_ID',[problemID])[0]
    tags = getProblemInfoAndHashtags(record[0])

    return record, tags
