import sqlite3

connection = sqlite3.connect("ifix_db_backup/AccessLevels.db")
cursor = connection.cursor()

def initDocTable():
    global cursor
    global connection
    cursor.execute("CREATE TABLE IF NOT EXISTS DOCUMENTS (ID INTEGER PRIMARY KEY AUTOINCREMENT, CON_UID INTEGER, DOCUMENT_NAME TEXT, FILENAME TEXT)")
    connection.commit()

def manufacturers():
    global cursor
    manufacturers = cursor.execute("SELECT * FROM MANUFACTURERS ORDER BY MFG_NAME ASC").fetchall()
    return manufacturers

def controllersFromID(MFG_UID):
    global cursor
    controllers = cursor.execute("SELECT * FROM CONTROLLERS WHERE MFG_UID = ? ORDER BY CONTROLLER_NAME ASC", (MFG_UID,),).fetchall()
    return controllers

def codesForControllerFromID(CON_UID):
    global cursor
    codes = cursor.execute("SELECT * FROM PASSWORDS WHERE CON_UID = ? ORDER BY ACCESS_LEVEL ASC", (CON_UID,),).fetchall()
    return codes

def controllerThumbFilenameFromID(CON_UID):
    global cursor
    filename = cursor.execute("SELECT PATH FROM THUMBS WHERE CON_UID = ?", (CON_UID,),).fetchall()
    if len(filename) > 0:
        return filename[0][0]
    else:
        return ""

def docsForControllerFromID(CON_UID):
    global cursor
    docs = cursor.execute("SELECT * FROM DOCUMENTS WHERE CON_UID = ? ORDER BY DOCUMENT_NAME ASC", (CON_UID,),).fetchall()
    return docs

def addManufacturer(manufacturer):
    global cursor
    global connection
    cursor.execute("INSERT INTO MANUFACTURERS (MFG_NAME) VALUES(?)", (manufacturer,),)
    connection.commit()

def addController(MFG_UID, controllerName):
    global cursor
    global connection
    cursor.execute("INSERT INTO CONTROLLERS (CONTROLLER_NAME, MFG_UID) VALUES(?,?)", (controllerName, MFG_UID),)
    connection.commit()

def addPassword(MFG_UID, CON_UID, passwordName):
    emptyPassword = ""
    global cursor
    global connection
    cursor.execute("INSERT INTO PASSWORDS (MFG_UID, CON_UID, ACCESS_LEVEL, DETAIL_DESCRIPTION) VALUES(?,?,?,?)", (MFG_UID, CON_UID, passwordName, emptyPassword),)
    connection.commit()

def addControllerDocument(CON_UID, description, filename):
    global connection
    global cursor
    cursor.execute("INSERT INTO DOCUMENTS (CON_UID, DOCUMENT_NAME, FILENAME) VALUES(?,?,?)", (CON_UID, description, filename),)
    connection.commit()

def updatePassword(MFG_UID, CON_UID, PASS_UID, name, details):
    global cursor
    global connection
    cursor.execute("INSERT OR REPLACE INTO PASSWORDS (ID, MFG_UID, CON_UID, ACCESS_LEVEL, DETAIL_DESCRIPTION) VALUES(?,?,?,?,?)", (PASS_UID, MFG_UID, CON_UID, name, details),)
    connection.commit()
