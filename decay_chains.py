#!/usr/bin/env python3
import sqlite3

"""
/////////////////////

Class Declarations

////////////////////
"""
class Nuclide:
#class contains nuclide info prev and next pointers as father and daughter
    def __init__(self, nuclide, half_life, decay_mode, daughter=None, father=None):
        self.nuclide = nuclide
        self.half_life = half_life
        self.decay_mode = decay_mode
        self.daughter = daughter
        self.father = father


class DecayChain:

    def __init__(self):
        self.headval = None

    def appendNuclide(self, nuclide, half_life, decay_mode, daughter=None, father=None):
        purpose = """ Used to append a nuclide to the end of the linked list.
        Usage: appendNuclide(nuclide, half_life, decay_mode, daughter, father)
        
        args:
        nuclide = nuclide to append 
        half_life = half life of the nuclide 
        decay_mode = mode of decay ie. alpha, beta, gama, positron ect.. 
        daughter = daughter product as a result of decay (if any)
        father = parent nuclide which the nuclide is a daughter of (if any)
        """

        try:
            newNuclide = Nuclide(nuclide, half_life, decay_mode, daughter, father)
            if self.headval is None:
                self.headval = newNuclide
                return
            last = self.headval
            while(last.daughter):
                last = last.daughter
            last.daughter = newNuclide
        except Exception as e:
            print(purpose, "\nError: ", e)

    def removeNuclide(self, key):
        purpose = """ Used to remove a nuclide from the chain.
        Usage: removeNuclide(key)

        args: key = nuclide to remove
        """
        try:
            headVal = self.headval
            if headVal != None:
                if headVal.nuclide == key:
                    self.head = headVal.daughter
                    headVal = None
                    return
            while headVal != None:
                if headVal.nuclide == key:
                    break
                prev = headVal
                headVal = headVal.daughter
            if headVal == None:
                return
            prev.daughter = headVal.daughter
            headVal = None
        except Exception as e:
            print(purpose, "\nError: ", e)

    def chainPrint(self):
        purpose = """ Used to print all the nodes in the DecayChain
        
        Usage: chainPrint()
        """
        try:
            printval = self.headval
            while printval != "None":
                print(printval.nuclide)
                if printval.decay_mode != "Stable":
                    print("Decays by {}".format(printval.decay_mode))
                    print("*"*10)
                else: 
                    print("End of Chain: Stable Element")               
                printval = printval.daughter
        except Exception as e:
            print(purpose, "\nError: ", e)


"""
/////////////////////

Functions

////////////////////
"""

def nodeGen(list):
        purpose = """pass in a list to generate nodes from the list items
        any list can be passed in.  I used the days of the week
        Usage: nodeGen(list)
        
        Args:
        list = [] any list"""
    
        try:
            for i in range(2, len(list)+1):
                print("d"+str(i) +' = Nuclide("'+list[i-1][0]+'", "'
                + list[i-1][1]+'"' + ', "' + list[i-1][2] +'"'+', "' 
                + list[i-1][3] +'", "'+ list[i-1][4] +'")')
        except Exception as e:
            print(purpose, "\nError: ", e)


def nextGen(list):
    purpose =  """used to generate the code for adding Node.nextval in the range of the list
    Usage: nextGen(list)

    Args:
    list = [] any list"""
    
    dlist = []
    try:
        for i in range(2,len(list)+1):
            dlist.append("d"+str(i))

        for d in range(len(dlist)-1):
            print(dlist[d]+".daughter = " + dlist[d+1]) 
    except Exception as e:
        print(purpose, "\nError: ", e)


"""
/////////////////////

Sqlite3 connection functions

////////////////////
"""
def createConn(db_file):
    purpose = """ Creates a database connection to sqlite db file passed in as an arg.
    Usage: createConn(db_file)

    args:
    db_file = database file 
    """
    try: 
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(purpose, "\nError: ", e)

def createTable(conn, create_table_sql_statement):
    purpose = """creates a table using the create_table_sql_statement
    Usage: createTable(conn, create_table_sql_statement)

    args:
    conn = connection object from createConn()
    create_table_sql_statement = 
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql_statement)
    except Exception as e:
        print(purpose, "Error: ", e)


def table_insert(conn, list, nodeList):
    purpose = """ insert data into two tables: "rn_decay" and "linked_list" using sql statements:
    Usage: table_insert(conn, list, nodeList)

    args:
    conn = connection from main
    list = dec (data for rn_decay)
    nodeLIst = nodeList (data for linked_list)
    """
    c = conn.cursor()
    try:
        for i in range(0, len(dec)):
            sql_statement_rad_decay = """INSERT INTO rn_decay (nuclide, half_life, decay_mode, daughter, father)
            VALUES("{0}", "{1}", "{2}", "{3}", "{4}")
            """.format(list[i][0], list[i][1], list[i][2], list[i][3], list[i][4])
            c.execute(sql_statement_rad_decay)
            
        inc = 0
        for i in range(0, len(nodeList)):
            sql_statement_linked_list = """INSERT INTO linked_list (node)
            VALUES("{}")
            """.format(nodeList[i])
            c.execute(sql_statement_linked_list)
    except Exception as e:
        print(purpose, "Error: ", e)
    

def displayData(conn, table):
    c = conn.cursor()
    sql = """SELECT * FROM {}
    """.format(table)
    try:
        c.execute(sql)
        rows = c.fetchall()
    except Exception as e:
        print("Error: ", e)
    for row in rows:
        print(row)

    """
////////////////////
Main Sqlite Connection
///////////////////
    """
def main_sql():
    purpose = """ opens database connection and creates tables to store nuclide data
    Usage: openDb()
    
    args: NONE
    """
    database = "rad_decay.db"

    sql_create_rn_decay = """CREATE TABLE IF NOT EXISTS rn_decay (
        id integer PRIMARY KEY AUTOINCREMENT,
        nuclide text NOT NULL,
        half_life text NOT NULL, 
        decay_mode text NOT NULL, 
        daughter text NOT NULL,
        father text NOT NULL
        )"""

    sql_create_linked_list_table = """CREATE TABLE IF NOT EXISTS linked_list(
        id integer PRIMARY KEY AUTOINCREMENT,
        node
        )
        """
    conn = createConn(database)
    if conn != None:
        createTable(conn, sql_create_rn_decay)
        createTable(conn, sql_create_linked_list_table)
    else: 
        print(purpose,"\nError:  Can't create DB connection")
    
    # populate tables
    table_insert(conn, dec, nodeList)

    # display a table
    print("SQLite table data:")
    displayData(conn, "rn_decay")
    print("\nNuclide Instances")
    print("*"*40)
    displayData(conn, "linked_list")

    # close db connection
    conn.commit()
    conn.close()
    


"""
/////////////////////

Main Code Starts here

////////////////////
"""
if __name__ == "__main__":
    dec = [
        ("Radon 222", "3.8 days", "Alpha", "Polonium 218", 'None'),
        ("Polonium 218", "3.1 minutes", "Alpha", "Lead 214", "Radon 222"),
        ("Lead 214", "27 minutes", "Beta", "Bismuth 214", "Polonium 218"), 
        ("Bismuth 214", "20 minutes", "Beta", "Polonium 214", "Lead 214"),
        ("Polonium 214", "160 uSec", "Alpha", "Lead 210", "Bismuth 214"),
        ("Lead 210", "22 years", "Beta", "Bismuth 210", "Polonium 214"),
        ("Polonium 210", "140 days", "Alpha", "Lead 206", "Bismuth 210"),
        ("Lead 206", "Stable", "Stable", 'None', "Polonium 210")
    ]

    rn = DecayChain()
    # nodeGen(dec)
    # nextGen(dec)

    rn.headval = Nuclide(dec[0][0],dec[0][1],dec[0][2],dec[0][3],dec[0][4])
    d2 = Nuclide("Polonium 218", "3.1 minutes", "Alpha", "Lead 214", "Radon 222")
    d3 = Nuclide("Lead 214", "27 minutes", "Beta", "Bismuth 214", "Polonium 218")
    d4 = Nuclide("Bismuth 214", "20 minutes", "Beta", "Polonium 214", "Lead 214")
    d5 = Nuclide("Polonium 214", "160 uSec", "Alpha", "Lead 210", "Bismuth 214")
    d6 = Nuclide("Lead 210", "22 years", "Beta", "Bismuth 210", "Polonium 214")
    d7 = Nuclide("Polonium 210", "140 days", "Alpha", "Lead 206", "Bismuth 210")
    d8 = Nuclide("Lead 206", "Stable", "Stable", "None", "Polonium 210")

    rn.headval.daughter = d2
    d2.daughter = d3
    d3.daughter = d4
    d4.daughter = d5
    d5.daughter = d6
    d6.daughter = d7
    d7.daughter = d8
   
    rn.chainPrint()
    nodeList = [rn.headval, d2, d3, d4, d5, d6, d7, d8]
    print("*"*40)
    print("*"*40,"\n\n")

    main_sql()
    
    
    