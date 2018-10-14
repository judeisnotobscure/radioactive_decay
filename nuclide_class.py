#!/usr/bin/env python3

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