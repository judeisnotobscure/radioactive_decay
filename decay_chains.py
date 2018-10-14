#!/usr/bin/env python3
import sqlite3
from sqlite_scratch import *
from nuclide_class import *



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
    
    print("""Radon is a naturally occuring radio isotope found in rocks and soil.
    \nIt contributes to our background radiation exposure.  
    \nHere is a look at what happens when the Radon emits radiation by radioactive decay\n""","*"*40)
    rn.chainPrint()
    nodeList = [rn.headval, d2, d3, d4, d5, d6, d7, d8]
    print("*"*40)
    print("*"*40,"\n\n")


    """
////////////////////
Main Sqlite Connection
///////////////////
    """
    sql_create_rn_decay = """CREATE TABLE IF NOT EXISTS rn_decay (
        id integer PRIMARY KEY AUTOINCREMENT,
        nuclide text NOT NULL,
        half_life text NOT NULL, 
        decay_mode text NOT NULL, 
        daughter text NOT NULL,
        father text NOT NULL)"""

    sql_create_linked_list_table = """CREATE TABLE IF NOT EXISTS linked_list(
        id integer PRIMARY KEY AUTOINCREMENT,
        node)"""

    sql_create_decay_mode_table = """CREATE TABLE IF NOT EXISTS decay_mode(
        id integer PRIMARY KEY AUTOINCREMENT,
        decay_id text NOT NULL,
        decay_type)"""

    sql_statement_read = """SELECT * FROM rn_decay JOIN decay_mode ON decay_mode.decay_id = rn_decay.decay_mode"""

    decay_mode_list = ["Alpha", "Beta", "Electron_Capture", "Neutron", "Stable"]

    decay = Sql("decay.db")
    decay.create_conn()
    decay.write_table(sql_create_rn_decay)
    decay.write_table(sql_create_linked_list_table)
    decay.write_table(sql_create_decay_mode_table) 
    for i in range(0, len(decay_mode_list)):
        decay.write_table("""INSERT INTO decay_mode (decay_id, decay_type)
        VALUES("{}", "{}")
        """.format(i+1, decay_mode_list[i]))

    for i in range(0, len(dec)):
        if dec[i][2] == "Alpha":
            decay_type = 1
        elif dec[i][2] == "Beta":
            decay_type = 2
        else:
            decay_type = 5
        decay.write_table("""INSERT INTO rn_decay (nuclide, half_life, decay_mode, daughter, father)
            VALUES("{0}", "{1}", "{2}", "{3}", "{4}")
            """.format(dec[i][0], dec[i][1], decay_type, dec[i][3], dec[i][4]))
    decay.write_table("""INSERT INTO linked_list (node)
            VALUES("{}")
            """.format(nodeList[i]))
    decay.read_table(sql_statement_read)
    decay.close_conn()